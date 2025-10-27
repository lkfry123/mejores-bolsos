#!/usr/bin/env python3
"""
GTM Deduplication Script - Removes duplicate GTM loaders

This script:
1. Finds all GTM loader blocks for the same container ID
2. Keeps only ONE GTM script in <head>
3. Ensures noscript iframe exists after <body>
4. Creates backups before modification
5. Reports summary of changes

Usage:
    python3 tools/gtm_dedupe_fix.py
"""

import os
import re
import shutil
from pathlib import Path

GTM_ID = "GTM-TCG7SMDD"
BACKUP_SUFFIX = ".bak_gtm_dedupe_fix"

# Canonical GTM blocks
GTM_HEAD = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start': new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0], j=d.createElement(s), dl=l!='dataLayer'?'&l='+l:'';j.async=true; j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

# Regex to find GTM blocks (flexible matching)
RE_GTM_BLOCK = re.compile(
    r"<!--\s*Google Tag Manager\s*-->.*?googletagmanager\.com/gtm\.js.*?<!--\s*End Google Tag Manager\s*-->",
    re.IGNORECASE | re.DOTALL
)

# Regex to find noscript blocks
RE_GTM_NOSCRIPT = re.compile(
    r"<!--\s*Google Tag Manager \(noscript\)\s*-->.*?googletagmanager\.com/ns\.html.*?<!--\s*End Google Tag Manager \(noscript\)\s*-->",
    re.IGNORECASE | re.DOTALL
)

def clean_gtm_duplicates(content: str) -> tuple[str, int]:
    """Remove all GTM blocks and return cleaned content + count of removed blocks."""
    original_content = content
    
    # Find all GTM blocks
    gtm_blocks = list(RE_GTM_BLOCK.finditer(content))
    
    if not gtm_blocks:
        return content, 0
    
    # Remove all GTM blocks (work backwards to maintain positions)
    for match in reversed(gtm_blocks):
        content = content[:match.start()] + content[match.end():]
    
    removed_count = len(gtm_blocks)
    return content, removed_count

def insert_single_gtm_head(content: str) -> str:
    """Insert a single canonical GTM script after <head> tag."""
    head_pattern = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
    match = head_pattern.search(content)
    
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + '\n' + GTM_HEAD + '\n' + content[insert_pos:]
    else:
        # If no <head>, prepend to content
        content = GTM_HEAD + '\n' + content
    
    return content

def ensure_noscript_after_body(content: str) -> tuple[str, bool]:
    """Ensure noscript iframe exists after <body> tag."""
    # Check if noscript already exists
    if RE_GTM_NOSCRIPT.search(content):
        return content, False
    
    body_pattern = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
    match = body_pattern.search(content)
    
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + '\n' + GTM_BODY + '\n' + content[insert_pos:]
        return content, True
    
    return content, False

def process_file(file_path: Path) -> tuple[str, str, int, bool]:
    """Process a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return str(file_path), f"error: {e}", 0, False
    
    original_content = content
    
    # Step 1: Remove all GTM blocks
    content, removed_count = clean_gtm_duplicates(content)
    
    # Step 2: Insert single GTM script in head
    content = insert_single_gtm_head(content)
    
    # Step 3: Ensure noscript after body
    content, added_noscript = ensure_noscript_after_body(content)
    
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
    return str(file_path), status, removed_count, added_noscript

def main():
    """Main execution."""
    print("=== GTM Deduplication Fix ===")
    print(f"GTM Container: {GTM_ID}")
    print(f"Backup suffix: {BACKUP_SUFFIX}")
    print()
    
    stats = {
        'processed': 0,
        'changed': 0,
        'total_duplicates_removed': 0,
        'noscript_added': 0,
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
        path, status, removed, added_noscript = process_file(file_path)
        
        if status == "updated":
            stats['changed'] += 1
            print(f"✅ {path}")
            if removed > 0:
                print(f"   Removed {removed} duplicate GTM block(s)")
            if added_noscript:
                print(f"   Added noscript iframe")
        elif status.startswith("error"):
            stats['errors'] += 1
            print(f"❌ {path} - {status}")
        else:
            print(f"⚪ {path} - no changes needed")
        
        stats['total_duplicates_removed'] += removed
        stats['noscript_added'] += 1 if added_noscript else 0
    
    # Print summary
    print()
    print("=== Summary ===")
    print(f"Files processed: {stats['processed']}")
    print(f"Files changed: {stats['changed']}")
    print(f"Duplicate GTM blocks removed: {stats['total_duplicates_removed']}")
    print(f"Noscript iframes added: {stats['noscript_added']}")
    print(f"Errors: {stats['errors']}")
    print()
    print("✅ GTM deduplication complete!")

if __name__ == "__main__":
    main()
