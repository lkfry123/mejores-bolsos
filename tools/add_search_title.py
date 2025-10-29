#!/usr/bin/env python3
"""
Update Search Bar with Title

This script updates the search bar HTML across all pages to include a title.
"""

import os
import re
from pathlib import Path

def update_search_bar_in_file(file_path):
    """Update search bar in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False
    
    # Check if search bar already has title
    if 'ah-search-title' in content:
        print(f"ℹ️  Search bar already has title in {file_path}")
        return True
    
    # Find the search form and add title
    pattern = r'(<form action="/search/" method="get" class="ah-search" role="search" aria-label="Site search">)'
    replacement = '''<div class="ah-search-container">
            <h3 class="ah-search-title">Search Affordable Handbags</h3>
            <form action="/search/" method="get" class="ah-search" role="search" aria-label="Site search">'''
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        
        # Also need to close the div after the form
        form_close_pattern = r'(</form>\s*<div class="hamburger">)'
        form_close_replacement = '''</form>
            </div>
            <div class="hamburger">'''
        
        new_content = re.sub(form_close_pattern, form_close_replacement, new_content)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Added search title to {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            return False
    else:
        print(f"⚠️  Could not find search form pattern in {file_path}")
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
    print("=== ADDING SEARCH TITLE TO ALL PAGES ===")
    print("Adding 'Search Affordable Handbags' title above search bar...")
    print()
    
    html_files = find_all_html_files()
    print(f"Found {len(html_files)} HTML files to process:")
    print()
    
    success_count = 0
    error_count = 0
    
    for file_path in html_files:
        if update_search_bar_in_file(file_path):
            success_count += 1
        else:
            error_count += 1
    
    print()
    print("=== SUMMARY ===")
    print(f"✅ Files processed successfully: {success_count}")
    print(f"❌ Files with errors: {error_count}")
    print(f"📁 Total files checked: {len(html_files)}")
    
    if error_count == 0:
        print("\n🎉 Search title added to all pages!")
    else:
        print(f"\n⚠️  {error_count} files had errors during processing")

if __name__ == "__main__":
    main()
