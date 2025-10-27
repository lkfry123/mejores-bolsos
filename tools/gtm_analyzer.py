#!/usr/bin/env python3
"""
Comprehensive GTM Analysis Script - Finds and reports all GTM implementations

This script:
1. Scans the entire project for GTM implementations
2. Identifies duplicates, missing implementations, and inconsistencies
3. Reports detailed findings for each file
4. Provides recommendations for fixes

Usage:
    python3 tools/gtm_analyzer.py
"""

import os
import re
from pathlib import Path
from collections import defaultdict

GTM_ID = "GTM-TCG7SMDD"

# Regex patterns for different GTM implementations
RE_GTM_SCRIPT = re.compile(
    r"<!--\s*Google Tag Manager\s*-->.*?googletagmanager\.com/gtm\.js.*?<!--\s*End Google Tag Manager\s*-->",
    re.IGNORECASE | re.DOTALL
)

RE_GTM_NOSCRIPT = re.compile(
    r"<!--\s*Google Tag Manager \(noscript\)\s*-->.*?googletagmanager\.com/ns\.html.*?<!--\s*End Google Tag Manager \(noscript\)\s*-->",
    re.IGNORECASE | re.DOTALL
)

RE_GTAG_SCRIPT = re.compile(
    r"<!--\s*Google tag \(gtag\.js\)\s*-->.*?googletagmanager\.com/gtag/js.*?<!--\s*End Google tag \(gtag\.js\)\s*-->",
    re.IGNORECASE | re.DOTALL
)

RE_GTAG_CONFIG = re.compile(
    r"gtag\('config',\s*['\"][^'\"]*['\"]\s*\)",
    re.IGNORECASE
)

RE_GTAG_INIT = re.compile(
    r"gtag\('js',\s*new Date\(\)\s*\)",
    re.IGNORECASE
)

def analyze_file(file_path: Path) -> dict:
    """Analyze a single HTML file for GTM implementations."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}
    
    analysis = {
        "file": str(file_path),
        "gtm_scripts": [],
        "gtm_noscripts": [],
        "gtag_scripts": [],
        "gtag_configs": [],
        "gtag_inits": [],
        "has_head": bool(re.search(r'<head[^>]*>', content, re.IGNORECASE)),
        "has_body": bool(re.search(r'<body[^>]*>', content, re.IGNORECASE)),
        "file_size": len(content),
        "lines": len(content.splitlines())
    }
    
    # Find GTM scripts
    for match in RE_GTM_SCRIPT.finditer(content):
        script_content = match.group(0)
        analysis["gtm_scripts"].append({
            "start": match.start(),
            "end": match.end(),
            "content": script_content[:100] + "..." if len(script_content) > 100 else script_content,
            "has_correct_id": GTM_ID in script_content
        })
    
    # Find GTM noscripts
    for match in RE_GTM_NOSCRIPT.finditer(content):
        noscript_content = match.group(0)
        analysis["gtm_noscripts"].append({
            "start": match.start(),
            "end": match.end(),
            "content": noscript_content[:100] + "..." if len(noscript_content) > 100 else noscript_content,
            "has_correct_id": GTM_ID in noscript_content
        })
    
    # Find gtag scripts
    for match in RE_GTAG_SCRIPT.finditer(content):
        gtag_content = match.group(0)
        analysis["gtag_scripts"].append({
            "start": match.start(),
            "end": match.end(),
            "content": gtag_content[:100] + "..." if len(gtag_content) > 100 else gtag_content
        })
    
    # Find gtag configs
    for match in RE_GTAG_CONFIG.finditer(content):
        analysis["gtag_configs"].append({
            "start": match.start(),
            "end": match.end(),
            "content": match.group(0)
        })
    
    # Find gtag inits
    for match in RE_GTAG_INIT.finditer(content):
        analysis["gtag_inits"].append({
            "start": match.start(),
            "end": match.end(),
            "content": match.group(0)
        })
    
    return analysis

def get_file_status(analysis: dict) -> str:
    """Determine the status of a file based on its GTM implementation."""
    if "error" in analysis:
        return "ERROR"
    
    gtm_count = len(analysis["gtm_scripts"])
    noscript_count = len(analysis["gtm_noscripts"])
    gtag_count = len(analysis["gtag_scripts"])
    
    if gtm_count == 0:
        return "NO_GTM"
    elif gtm_count == 1 and noscript_count == 1:
        return "PERFECT"
    elif gtm_count == 1 and noscript_count == 0:
        return "MISSING_NOSCRIPT"
    elif gtm_count > 1:
        return "DUPLICATE_GTM"
    elif gtag_count > 0:
        return "HAS_GTAG"
    else:
        return "UNKNOWN"

def main():
    """Main analysis function."""
    print("=== Comprehensive GTM Analysis ===")
    print(f"GTM Container ID: {GTM_ID}")
    print()
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk("."):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools'}]
        
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files to analyze")
    print()
    
    # Analyze each file
    analyses = []
    status_counts = defaultdict(int)
    
    for file_path in sorted(html_files):
        analysis = analyze_file(file_path)
        analyses.append(analysis)
        status = get_file_status(analysis)
        status_counts[status] += 1
    
    # Print detailed results
    print("=== Detailed Analysis Results ===")
    print()
    
    for analysis in analyses:
        status = get_file_status(analysis)
        file_path = analysis["file"]
        
        if status == "ERROR":
            print(f"❌ {file_path} - ERROR: {analysis['error']}")
        elif status == "PERFECT":
            print(f"✅ {file_path} - PERFECT (1 GTM script, 1 noscript)")
        elif status == "DUPLICATE_GTM":
            print(f"⚠️  {file_path} - DUPLICATE GTM ({len(analysis['gtm_scripts'])} scripts)")
            for i, script in enumerate(analysis["gtm_scripts"]):
                correct_id = "✅" if script["has_correct_id"] else "❌"
                print(f"    Script {i+1}: {correct_id} {script['content'][:50]}...")
        elif status == "MISSING_NOSCRIPT":
            print(f"⚠️  {file_path} - MISSING NOSCRIPT (1 GTM script, 0 noscript)")
        elif status == "HAS_GTAG":
            print(f"⚠️  {file_path} - HAS GTAG ({len(analysis['gtag_scripts'])} gtag scripts)")
        elif status == "NO_GTM":
            print(f"❌ {file_path} - NO GTM IMPLEMENTATION")
        else:
            print(f"❓ {file_path} - UNKNOWN STATUS")
    
    # Print summary
    print()
    print("=== Summary ===")
    print(f"Total files analyzed: {len(html_files)}")
    print(f"Perfect implementations: {status_counts['PERFECT']}")
    print(f"Duplicate GTM scripts: {status_counts['DUPLICATE_GTM']}")
    print(f"Missing noscript: {status_counts['MISSING_NOSCRIPT']}")
    print(f"Has gtag (should be removed): {status_counts['HAS_GTAG']}")
    print(f"No GTM implementation: {status_counts['NO_GTM']}")
    print(f"Errors: {status_counts['ERROR']}")
    print(f"Unknown status: {status_counts['UNKNOWN']}")
    
    # Recommendations
    print()
    print("=== Recommendations ===")
    if status_counts['DUPLICATE_GTM'] > 0:
        print(f"🔧 Fix {status_counts['DUPLICATE_GTM']} files with duplicate GTM scripts")
    if status_counts['MISSING_NOSCRIPT'] > 0:
        print(f"🔧 Add noscript to {status_counts['MISSING_NOSCRIPT']} files")
    if status_counts['HAS_GTAG'] > 0:
        print(f"🔧 Remove gtag from {status_counts['HAS_GTAG']} files")
    if status_counts['NO_GTM'] > 0:
        print(f"🔧 Add GTM to {status_counts['NO_GTM']} files")
    
    if status_counts['PERFECT'] == len(html_files):
        print("🎉 All files have perfect GTM implementation!")
    else:
        print(f"📊 {status_counts['PERFECT']}/{len(html_files)} files are perfect")

if __name__ == "__main__":
    main()
