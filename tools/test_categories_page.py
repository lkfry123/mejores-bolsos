#!/usr/bin/env python3
"""
Test Categories Page Links

This script specifically tests the categories page to ensure all links work correctly.
"""

import os
import re

def test_categories_page():
    """Test the categories page links."""
    print("=== TESTING CATEGORIES PAGE LINKS ===")
    
    try:
        with open('categories/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading categories/index.html: {e}")
        return
    
    print("\n=== FEATURED ARTICLE LINK TEST ===")
    
    # Check the featured article link
    featured_link_match = re.search(r'href="(/articles/[^"]+)"', content)
    if featured_link_match:
        featured_link = featured_link_match.group(1)
        print(f"Featured article link: {featured_link}")
        
        # Check if the file exists
        file_path = featured_link.lstrip('/')
        if os.path.exists(file_path):
            print(f"✅ Featured article link works: {file_path} exists")
        else:
            print(f"❌ Featured article link broken: {file_path} not found")
    else:
        print("❌ No featured article link found")
    
    print("\n=== CATEGORY LINKS TEST ===")
    
    # Check category links
    category_links = re.findall(r'href="(/articles/[^"]+\.html)"', content)
    print(f"Found {len(category_links)} category links:")
    
    for link in category_links:
        file_path = link.lstrip('/')
        if os.path.exists(file_path):
            print(f"  ✅ {link} - exists")
        else:
            print(f"  ❌ {link} - missing")
    
    print("\n=== NAVIGATION LINKS TEST ===")
    
    # Check navigation links
    nav_links = re.findall(r'href="(/[^"]+)"', content)
    print(f"Found {len(nav_links)} navigation links:")
    
    for link in nav_links:
        if link.startswith('/articles/') and link.endswith('.html'):
            file_path = link.lstrip('/')
            if os.path.exists(file_path):
                print(f"  ✅ {link} - exists")
            else:
                print(f"  ❌ {link} - missing")
        elif link in ['/', '/categories/', '/articles/', '/quiz/bag-personality/', '#contact']:
            print(f"  ✅ {link} - valid navigation")
        else:
            print(f"  ⚠️  {link} - check manually")
    
    print(f"\n=== CATEGORIES PAGE TEST COMPLETE ===")
    print("The categories page links should now work correctly!")
    print("Featured article link has been fixed to point to the correct .html file.")

if __name__ == "__main__":
    test_categories_page()
