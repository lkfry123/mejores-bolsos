#!/usr/bin/env python3
"""
GTM Cleanup Script - Removes all remaining gtag.js implementations

This script:
1. Removes all direct gtag.js script blocks
2. Removes all gtag() function calls
3. Removes all GA4 measurement ID references
4. Keeps only the GTM implementation
5. Creates backups before modification

Usage:
    python3 tools/gtm_cleanup.py
"""

import os
import re
import shutil
from pathlib import Path

GTM_ID = "GTM-TCG7SMDD"
GA4_ID = "G-H1Q1KL01RP"
BACKUP_SUFFIX = ".bak_gtm_cleanup"

# Regex patterns for gtag cleanup
RE_GTAG_SCRIPT = re.compile(
    r"<!--\s*Google tag \(gtag\.js\)\s*-->.*?<!--\s*End Google tag \(gtag\.js\)\s*-->",
    re.IGNORECASE | re.DOTALL
)

RE_GTAG_INLINE = re.compile(
    r"<script[^>]*>.*?gtag\(.*?</script>",
    re.IGNORECASE | re.DOTALL
)

RE_GTAG_FUNCTION = re.compile(
    r"function gtag\(\)\{[^}]*\}",
    re.IGNORECASE
)

RE_GTAG_CALLS = re.compile(
    r"gtag\('[^']*',\s*[^)]*\)",
    re.IGNORECASE
)

RE_GTAG_JS_INIT = re.compile(
    r"gtag\('js',\s*new Date\(\)\s*\)",
    re.IGNORECASE
)

RE_DATA_LAYER_INIT = re.compile(
    r"window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];",
    re.IGNORECASE
)

RE_GA4_COMMENTS = re.compile(
    r"<!--\s*GA4 is configured in GTM.*?G-H1Q1KL01RP.*?-->",
    re.IGNORECASE | re.DOTALL
)

def clean_gtag_implementations(content: str) -> tuple[str, int]:
    """Remove all gtag.js implementations and return cleaned content + count of removals."""
    original_content = content
    removal_count = 0
    
    # Remove gtag script blocks
    content = RE_GTAG_SCRIPT.sub("", content)
    if content != original_content:
        removal_count += 1
        original_content = content
    
    # Remove inline gtag scripts
    content = RE_GTAG_INLINE.sub("", content)
    if content != original_content:
        removal_count += 1
        original_content = content
    
    # Remove gtag function definitions
    content = RE_GTAG_FUNCTION.sub("", content)
    if content != original_content:
        removal_count += 1
        original_content = content
    
    # Remove gtag calls
    content = RE_GTAG_CALLS.sub("", content)
    if content != original_content:
        removal_count += 1
        original_content = content
    
    # Remove gtag js init
    content = RE_GTAG_JS_INIT.sub("", content)
    if content != original_content:
        removal_count += 1
        original_content = content
    
    # Remove dataLayer initialization
    content = RE_DATA_LAYER_INIT.sub("", content)
    if content != original_content:
        removal_count += 1
        original_content = content
    
    # Remove GA4 comment blocks
    content = RE_GA4_COMMENTS.sub("", content)
    if content != original_content:
        removal_count += 1
        original_content = content
    
    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = re.sub(r'^\s*\n', '', content, flags=re.MULTILINE)
    
    return content, removal_count

def process_file(file_path: Path) -> tuple[str, str, int]:
    """Process a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return str(file_path), f"error: {e}", 0
    
    original_content = content
    
    # Clean gtag implementations
    content, removal_count = clean_gtag_implementations(content)
    
    # Check if content changed
    changed = (content != original_content)
    
    if changed:
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + BACKUP_SUFFIX)
        try:
            shutil.copy2(file_path, backup_path)
        except Exception:
            pass
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    status = "updated" if changed else "no_change"
    return str(file_path), status, removal_count

def main():
    """Main execution."""
    print("=== GTM Cleanup - Remove gtag.js Implementations ===")
    print(f"GTM Container: {GTM_ID}")
    print(f"GA4 Measurement ID: {GA4_ID}")
    print(f"Backup suffix: {BACKUP_SUFFIX}")
    print()
    
    stats = {
        'processed': 0,
        'changed': 0,
        'total_removals': 0,
        'errors': 0
    }
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk("."):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools'}]
        
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files to process")
    print()
    
    # Process each file
    for file_path in sorted(html_files):
        stats['processed'] += 1
        path, status, removals = process_file(file_path)
        
        if status == "updated":
            stats['changed'] += 1
            print(f"✅ {path}")
            if removals > 0:
                print(f"   Removed {removals} gtag implementation(s)")
        elif status.startswith("error"):
            stats['errors'] += 1
            print(f"❌ {path} - {status}")
        else:
            print(f"⚪ {path} - no gtag found")
        
        stats['total_removals'] += removals
    
    # Print summary
    print()
    print("=== Summary ===")
    print(f"Files processed: {stats['processed']}")
    print(f"Files changed: {stats['changed']}")
    print(f"Total gtag implementations removed: {stats['total_removals']}")
    print(f"Errors: {stats['errors']}")
    print()
    print("✅ GTM cleanup complete!")

if __name__ == "__main__":
    main()
