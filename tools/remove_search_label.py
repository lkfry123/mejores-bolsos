#!/usr/bin/env python3
"""
Remove Search Label

This script removes the screen reader label that says "Search" from all pages
since we now have the visible title above the search bar.
"""

import os
import re
from pathlib import Path

def remove_search_label(file_path):
    """Remove search label from a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False
    
    # Check if file has the search label
    if '<label for="site-search" class="sr-only">Search</label>' in content:
        # Remove the label line entirely
        new_content = content.replace('<label for="site-search" class="sr-only">Search</label>', '')
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Removed search label from {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            return False
    else:
        print(f"ℹ️  {file_path}: No search label found")
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
    print("=== REMOVING SEARCH LABEL ===")
    print("Removing 'Search' label from all pages...")
    print()
    
    html_files = find_all_html_files()
    print(f"Found {len(html_files)} HTML files to process:")
    print()
    
    success_count = 0
    error_count = 0
    
    for file_path in html_files:
        if remove_search_label(file_path):
            success_count += 1
        else:
            error_count += 1
    
    print()
    print("=== SUMMARY ===")
    print(f"✅ Files processed successfully: {success_count}")
    print(f"❌ Files with errors: {error_count}")
    print(f"📁 Total files checked: {len(html_files)}")
    
    if error_count == 0:
        print("\n🎉 Search label removed from all pages!")
        print("Now only the visible title 'Search Affordable Handbags' appears above the search bar.")
    else:
        print(f"\n⚠️  {error_count} files had errors during processing")

if __name__ == "__main__":
    main()
