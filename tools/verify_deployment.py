#!/usr/bin/env python3
"""
GTM Deployment Verification Script

This script helps verify that your GTM implementation is clean
and ready for deployment.

Usage:
    python3 tools/verify_deployment.py
"""

import os
import re
from pathlib import Path

def verify_file(file_path: Path) -> dict:
    """Verify a single HTML file for clean GTM implementation."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}
    
    # Check for GTM script
    gtm_script_count = len(re.findall(r'googletagmanager\.com/gtm\.js', content, re.IGNORECASE))
    
    # Check for GTM noscript
    gtm_noscript_count = len(re.findall(r'googletagmanager\.com/ns\.html', content, re.IGNORECASE))
    
    # Check for gtag (should be 0)
    gtag_count = len(re.findall(r'gtag\(', content, re.IGNORECASE))
    
    # Check for GA4 ID (should be 0)
    ga4_id_count = len(re.findall(r'G-H1Q1KL01RP', content))
    
    return {
        "gtm_scripts": gtm_script_count,
        "gtm_noscripts": gtm_noscript_count,
        "gtag_calls": gtag_count,
        "ga4_references": ga4_id_count,
        "is_clean": gtm_script_count == 1 and gtm_noscript_count == 1 and gtag_count == 0 and ga4_id_count == 0
    }

def main():
    """Main verification function."""
    print("=== GTM Deployment Verification ===")
    print()
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools'}]
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(Path(root) / file)
    
    print(f"Verifying {len(html_files)} HTML files...")
    print()
    
    clean_files = 0
    total_files = 0
    
    for file_path in sorted(html_files):
        total_files += 1
        result = verify_file(file_path)
        
        if "error" in result:
            print(f"❌ {file_path} - ERROR: {result['error']}")
        elif result["is_clean"]:
            clean_files += 1
            print(f"✅ {file_path} - CLEAN")
        else:
            print(f"⚠️  {file_path} - ISSUES:")
            print(f"    GTM scripts: {result['gtm_scripts']} (should be 1)")
            print(f"    GTM noscripts: {result['gtm_noscripts']} (should be 1)")
            print(f"    gtag calls: {result['gtag_calls']} (should be 0)")
            print(f"    GA4 references: {result['ga4_references']} (should be 0)")
    
    print()
    print("=== Summary ===")
    print(f"Total files: {total_files}")
    print(f"Clean files: {clean_files}")
    print(f"Files with issues: {total_files - clean_files}")
    
    if clean_files == total_files:
        print()
        print("🎉 ALL FILES ARE CLEAN AND READY FOR DEPLOYMENT!")
        print()
        print("Next steps:")
        print("1. Deploy these files to your live server")
        print("2. Clear CDN/cache if applicable")
        print("3. Test in Safari with hard refresh (Cmd+Shift+R)")
        print("4. Check Safari Developer Tools → Console for errors")
    else:
        print()
        print("⚠️  Some files need attention before deployment.")

if __name__ == "__main__":
    main()
