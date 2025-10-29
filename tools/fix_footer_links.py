#!/usr/bin/env python3
"""
Footer Link Fixer

This script fixes footer links across all HTML pages to ensure consistency
and proper local development compatibility.
"""

import os
import re
from pathlib import Path

def fix_footer_links_in_file(file_path):
    """Fix footer links in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False
    
    original_content = content
    
    # Fix category links
    content = re.sub(
        r'href="/articles/handbags/"',
        'href="/articles/handbags.html"',
        content
    )
    content = re.sub(
        r'href="/articles/backpacks/"',
        'href="/articles/backpacks.html"',
        content
    )
    content = re.sub(
        r'href="/articles/wallets/"',
        'href="/articles/wallets.html"',
        content
    )
    content = re.sub(
        r'href="/articles/tote-bags/"',
        'href="/articles/tote-bags.html"',
        content
    )
    
    # Fix legal links
    content = re.sub(
        r'href="/privacy-policy/"',
        'href="/privacy-policy.html"',
        content
    )
    content = re.sub(
        r'href="/affiliate-disclosure/"',
        'href="/affiliate-disclosure.html"',
        content
    )
    
    # Check if any changes were made
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed footer links in {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            return False
    else:
        print(f"ℹ️  No changes needed in {file_path}")
        return True

def find_all_html_files():
    """Find all HTML files in the project."""
    html_files = []
    for root, dirs, files in os.walk("."):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools', 'scripts'}]
        
        for file in files:
            if file.endswith('.html') and not file.startswith('.') and '.bak_' not in file:
                html_files.append(Path(root) / file)
    
    return html_files

def main():
    """Main execution."""
    print("=== FOOTER LINK FIXER ===")
    print("Fixing footer links across all HTML pages...")
    print()
    
    html_files = find_all_html_files()
    print(f"Found {len(html_files)} HTML files to check:")
    print()
    
    fixed_count = 0
    error_count = 0
    
    for file_path in html_files:
        if fix_footer_links_in_file(file_path):
            fixed_count += 1
        else:
            error_count += 1
    
    print()
    print("=== SUMMARY ===")
    print(f"✅ Files processed successfully: {fixed_count}")
    print(f"❌ Files with errors: {error_count}")
    print(f"📁 Total files checked: {len(html_files)}")
    
    if error_count == 0:
        print("\n🎉 All footer links have been fixed!")
    else:
        print(f"\n⚠️  {error_count} files had errors during processing")

if __name__ == "__main__":
    main()
