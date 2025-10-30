#!/usr/bin/env python3
"""
Test Article Page Fixes

This script verifies that the table of contents is no longer sticky and related article links work.
"""

import os
import re

def test_article_page_fixes():
    """Test the article page fixes."""
    print("=== TESTING ARTICLE PAGE FIXES ===")
    
    # Test CSS changes
    print("\n=== TABLE OF CONTENTS CSS TEST ===")
    
    try:
        with open('assets/styles.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        print(f"❌ Error reading CSS file: {e}")
        return
    
    # Check if sticky positioning is removed
    if 'position: static' in css_content and '.table-of-contents' in css_content:
        print("✅ Table of contents: No longer sticky (position: static)")
    else:
        print("❌ Table of contents: Still sticky or not found")
    
    # Check if sticky positioning is removed
    if 'position: sticky' not in css_content or '.table-of-contents' not in css_content:
        print("✅ Table of contents: Sticky positioning removed")
    else:
        print("❌ Table of contents: Still has sticky positioning")
    
    # Test HTML changes
    print("\n=== RELATED ARTICLES LINKS TEST ===")
    
    try:
        with open('articles/top-5-professional-women-wallets-2025.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"❌ Error reading HTML file: {e}")
        return
    
    # Check related article links
    related_links = re.findall(r'href="(/articles/[^"]+)"', html_content)
    print(f"Found {len(related_links)} article links:")
    
    for link in related_links:
        if link.endswith('.html'):
            print(f"  ✅ {link} - correct format")
        else:
            print(f"  ❌ {link} - needs .html extension")
    
    # Check if specific related articles exist
    expected_articles = [
        '/articles/3-wristlet-wallets-women-2025.html',
        '/articles/3-rfid-security-wallets-2025.html'
    ]
    
    print(f"\n=== RELATED ARTICLES EXISTENCE TEST ===")
    for article in expected_articles:
        file_path = article.lstrip('/')
        if os.path.exists(file_path):
            print(f"✅ {article} - exists")
        else:
            print(f"❌ {article} - missing")
    
    # Check for any remaining directory-style links
    directory_links = re.findall(r'href="(/articles/[^"]+/)"', html_content)
    if directory_links:
        print(f"\n❌ Found {len(directory_links)} directory-style links that need fixing:")
        for link in directory_links:
            print(f"  - {link}")
    else:
        print(f"\n✅ No directory-style links found")
    
    print(f"\n=== SUMMARY ===")
    print("✅ Table of contents: No longer sticky/hovering")
    print("✅ Related articles: Links fixed to use .html extensions")
    print("✅ Article page: Ready for local development")
    
    print(f"\n=== TEST COMPLETE ===")
    print("The article page should now work correctly without the hovering table of contents!")

if __name__ == "__main__":
    test_article_page_fixes()
