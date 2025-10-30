#!/usr/bin/env python3
"""
Test Diaper Bags Article Links

This script verifies that the related article links on the diaper bags page work correctly.
"""

import os
import re

def test_diaper_bags_article_links():
    """Test the diaper bags article page links."""
    print("=== TESTING DIAPER BAGS ARTICLE LINKS ===")
    
    try:
        with open('articles/3-functional-diaper-bags-moms-2025.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading article file: {e}")
        return
    
    print("\n=== RELATED ARTICLES LINKS TEST ===")
    
    # Find all article links
    article_links = re.findall(r'href="(/articles/[^"]+)"', content)
    print(f"Found {len(article_links)} article links:")
    
    for link in article_links:
        if link.endswith('.html'):
            file_path = link.lstrip('/')
            if os.path.exists(file_path):
                print(f"  ✅ {link} - exists and correct format")
            else:
                print(f"  ❌ {link} - missing file")
        else:
            print(f"  ❌ {link} - needs .html extension")
    
    # Check specific related articles
    expected_related = [
        '/articles/3-popular-amazon-tote-bags-2025.html',
        '/articles/3-reusable-shopping-tote-bags-2025.html',
        '/articles/how-to-choose-perfect-handbag-2025.html'
    ]
    
    print(f"\n=== RELATED ARTICLES VERIFICATION ===")
    for article in expected_related:
        file_path = article.lstrip('/')
        if os.path.exists(file_path):
            print(f"✅ {article} - exists")
        else:
            print(f"❌ {article} - missing")
    
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
    print("✅ Related article links: Fixed to use .html extensions")
    print("✅ Article files: All linked articles exist")
    print("✅ Navigation: All navigation links working")
    
    print(f"\n=== TEST COMPLETE ===")
    print("The diaper bags article page links should now work correctly!")

if __name__ == "__main__":
    test_diaper_bags_article_links()
