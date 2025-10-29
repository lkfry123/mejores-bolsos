#!/usr/bin/env python3
"""
Add Search Bar to All Pages

This script adds the search bar to the navigation of all HTML pages.
"""

import os
import re
from pathlib import Path

def add_search_bar_to_file(file_path):
    """Add search bar to a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False
    
    # Check if search bar already exists
    if 'ah-search' in content:
        print(f"ℹ️  Search bar already exists in {file_path}")
        return True
    
    # Find the nav-menu closing tag and add search bar before hamburger
    pattern = r'(</ul>\s*<div class="hamburger">)'
    replacement = '''</ul>
            <form action="/search/" method="get" class="ah-search" role="search" aria-label="Site search">
                <label for="site-search" class="sr-only">Search Affordable Handbags</label>
                <input id="site-search" name="q" type="text" placeholder="Search bags, brands, guides…" class="ah-search__input">
                <button type="submit" class="ah-search__btn" aria-label="Search">🔍</button>
            </form>
            <div class="hamburger">'''
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Added search bar to {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            return False
    else:
        print(f"⚠️  Could not find nav-menu pattern in {file_path}")
        return False

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
    print("=== ADDING SEARCH BAR TO ALL PAGES ===")
    print("Adding search bar to navigation across all HTML pages...")
    print()
    
    html_files = find_all_html_files()
    print(f"Found {len(html_files)} HTML files to process:")
    print()
    
    success_count = 0
    error_count = 0
    
    for file_path in html_files:
        if add_search_bar_to_file(file_path):
            success_count += 1
        else:
            error_count += 1
    
    print()
    print("=== SUMMARY ===")
    print(f"✅ Files processed successfully: {success_count}")
    print(f"❌ Files with errors: {error_count}")
    print(f"📁 Total files checked: {len(html_files)}")
    
    if error_count == 0:
        print("\n🎉 Search bar added to all pages!")
    else:
        print(f"\n⚠️  {error_count} files had errors during processing")

if __name__ == "__main__":
    main()
