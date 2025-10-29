#!/usr/bin/env python3
"""
Search Page Test

This script tests the search page by checking if it loads correctly.
"""

import os
import re

def test_search_page():
    """Test the search page."""
    print("=== TESTING SEARCH PAGE ===")
    
    search_page = "search/index.html"
    
    if not os.path.exists(search_page):
        print(f"❌ Search page not found: {search_page}")
        return False
    
    try:
        with open(search_page, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading search page: {e}")
        return False
    
    # Check for required elements
    required_elements = [
        ('<form action="/search/"', 'Search form'),
        ('id="results"', 'Results container'),
        ('id="suggestions"', 'Suggestions container'),
        ('fetch(\'/search-index.json\'', 'Search index fetch'),
        ('class="ah-search"', 'Search bar styles'),
        ('aria-label="Site search"', 'Accessibility label'),
        ('<label for="site-search"', 'Search input label')
    ]
    
    print("\n=== REQUIRED ELEMENTS CHECK ===")
    all_present = True
    
    for element, description in required_elements:
        if element in content:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            all_present = False
    
    # Check for proper HTML structure
    print("\n=== HTML STRUCTURE CHECK ===")
    
    if '<!doctype html>' in content:
        print("✅ Proper DOCTYPE")
    else:
        print("❌ Missing DOCTYPE")
        all_present = False
    
    if '<title>Search • Affordable Handbags</title>' in content:
        print("✅ Proper title")
    else:
        print("❌ Missing or incorrect title")
        all_present = False
    
    if 'lang="en"' in content:
        print("✅ Language attribute")
    else:
        print("❌ Missing language attribute")
        all_present = False
    
    # Check for accessibility
    print("\n=== ACCESSIBILITY CHECK ===")
    
    if 'role="search"' in content:
        print("✅ Search role attribute")
    else:
        print("❌ Missing search role")
        all_present = False
    
    if 'sr-only' in content:
        print("✅ Screen reader labels")
    else:
        print("❌ Missing screen reader labels")
        all_present = False
    
    # Check for mobile responsiveness
    print("\n=== MOBILE RESPONSIVENESS CHECK ===")
    
    if 'max-width:768px' in content or 'max-width: 768px' in content:
        print("✅ Mobile breakpoint defined")
    else:
        print("❌ Missing mobile breakpoint")
        all_present = False
    
    if 'flex:1' in content:
        print("✅ Flexible input sizing")
    else:
        print("❌ Missing flexible input sizing")
        all_present = False
    
    print(f"\n=== OVERALL RESULT ===")
    if all_present:
        print("🎉 Search page is properly configured!")
        return True
    else:
        print("⚠️  Search page has some issues")
        return False

if __name__ == "__main__":
    test_search_page()
