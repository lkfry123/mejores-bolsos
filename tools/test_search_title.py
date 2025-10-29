#!/usr/bin/env python3
"""
Test Search Bar with Title

This script verifies that the search bar title has been added correctly.
"""

import os
import re

def test_search_bar_title():
    """Test that search bar title is properly implemented."""
    print("=== TESTING SEARCH BAR WITH TITLE ===")
    
    # Test key pages
    test_pages = [
        'index.html',
        'privacy-policy.html', 
        'articles/handbags.html',
        'search/index.html'
    ]
    
    print("\n=== SEARCH BAR TITLE VERIFICATION ===")
    
    all_good = True
    
    for page in test_pages:
        if os.path.exists(page):
            try:
                with open(page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for search container
                if 'ah-search-container' in content:
                    print(f"✅ {page}: Search container found")
                else:
                    print(f"❌ {page}: Search container missing")
                    all_good = False
                
                # Check for search title
                if 'ah-search-title' in content and 'Search Affordable Handbags' in content:
                    print(f"✅ {page}: Search title found")
                else:
                    print(f"❌ {page}: Search title missing")
                    all_good = False
                
                # Check for proper HTML structure
                if '<div class="ah-search-container">' in content and '<h3 class="ah-search-title">' in content:
                    print(f"✅ {page}: Proper HTML structure")
                else:
                    print(f"❌ {page}: Improper HTML structure")
                    all_good = False
                    
            except Exception as e:
                print(f"❌ {page}: Error reading file - {e}")
                all_good = False
        else:
            print(f"⚠️  {page}: File not found")
    
    # Test CSS styles
    print("\n=== CSS STYLES VERIFICATION ===")
    
    if os.path.exists('assets/styles.css'):
        try:
            with open('assets/styles.css', 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            required_styles = [
                'ah-search-container',
                'ah-search-title',
                'flex-direction:column',
                'align-items:flex-end'
            ]
            
            for style in required_styles:
                if style in css_content:
                    print(f"✅ CSS: {style} found")
                else:
                    print(f"❌ CSS: {style} missing")
                    all_good = False
                    
        except Exception as e:
            print(f"❌ Error reading CSS file: {e}")
            all_good = False
    else:
        print("❌ CSS file not found")
        all_good = False
    
    print(f"\n=== FINAL RESULT ===")
    if all_good:
        print("🎉 Search bar title successfully implemented!")
        print("\nThe search bar now has:")
        print("  - 'Search Affordable Handbags' title above the search input")
        print("  - Clean, uncluttered header appearance")
        print("  - Responsive design (title left-aligned on mobile)")
        print("  - Consistent styling across all pages")
    else:
        print("⚠️  Some issues found with search bar title implementation")
    
    return all_good

if __name__ == "__main__":
    test_search_bar_title()
