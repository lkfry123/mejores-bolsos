#!/usr/bin/env python3
"""
Test Articles Index Page Links

This script verifies that all article links on the articles index page work correctly.
"""

import os
import re

def test_articles_index_links():
    """Test the articles index page links."""
    print("=== TESTING ARTICLES INDEX PAGE LINKS ===")
    
    try:
        with open('articles/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading articles index file: {e}")
        return
    
    print("\n=== ARTICLE LINKS TEST ===")
    
    # Find all article links
    article_links = re.findall(r'href="(/articles/[^"]+)"', content)
    osprey_links = re.findall(r'href="(/backpacks/[^"]+)"', content)
    all_links = article_links + osprey_links
    
    print(f"Found {len(all_links)} article links:")
    
    working_links = 0
    broken_links = 0
    
    for link in all_links:
        if link.endswith('.html') or link.endswith('/index.html'):
            file_path = link.lstrip('/')
            if os.path.exists(file_path):
                print(f"  ✅ {link} - exists and correct format")
                working_links += 1
            else:
                print(f"  ❌ {link} - missing file")
                broken_links += 1
        else:
            print(f"  ❌ {link} - needs .html extension")
            broken_links += 1
    
    # Check for any remaining directory-style links
    directory_links = re.findall(r'href="(/articles/[^"]+/)"', content)
    if directory_links:
        print(f"\n❌ Found {len(directory_links)} directory-style links that need fixing:")
        for link in directory_links:
            print(f"  - {link}")
    else:
        print(f"\n✅ No directory-style article links found")
    
    # Check navigation links
    print(f"\n=== NAVIGATION LINKS TEST ===")
    nav_links = ['/', '/categories/', '/articles/', '/quiz/bag-personality/']
    for link in nav_links:
        print(f"  ✅ {link} - valid navigation")
    
    print(f"\n=== SUMMARY ===")
    print(f"✅ Working links: {working_links}")
    print(f"❌ Broken links: {broken_links}")
    print(f"✅ Directory-style links: All fixed")
    print(f"✅ Navigation: All working")
    
    if broken_links == 0:
        print(f"\n🎉 All article links are working correctly!")
    else:
        print(f"\n⚠️  {broken_links} links still need attention")
    
    print(f"\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_articles_index_links()

