#!/usr/bin/env python3
"""
Test Search Bar Positioning

This script verifies that the search bar is positioned correctly with:
- Search bar moved slightly to the right
- Search label centered above the search bar
"""

import os
import re

def test_search_bar_positioning():
    """Test search bar positioning and styling."""
    print("=== TESTING SEARCH BAR POSITIONING ===")
    
    # Check CSS changes
    print("\n=== CSS VERIFICATION ===")
    
    css_file = "assets/styles.css"
    if os.path.exists(css_file):
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Check for updated container styles
            if 'align-items:center' in css_content and 'margin-left:20px' in css_content:
                print("✅ Search container: Centered alignment with right margin")
            else:
                print("❌ Search container: Missing center alignment or right margin")
            
            # Check for centered title
            if 'text-align:center' in css_content:
                print("✅ Search title: Centered text alignment")
            else:
                print("❌ Search title: Missing center alignment")
            
            # Check for mobile responsiveness
            if 'margin-left:0' in css_content and 'align-items:stretch' in css_content:
                print("✅ Mobile responsive: Proper mobile adjustments")
            else:
                print("❌ Mobile responsive: Missing mobile adjustments")
                
        except Exception as e:
            print(f"❌ Error reading CSS file: {e}")
    else:
        print("❌ CSS file not found")
    
    # Check HTML structure
    print("\n=== HTML STRUCTURE VERIFICATION ===")
    
    test_pages = [
        'index.html',
        'privacy-policy.html',
        'articles/handbags.html'
    ]
    
    for page in test_pages:
        if os.path.exists(page):
            try:
                with open(page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for proper container structure
                if 'ah-search-container' in content and 'ah-search-title' in content:
                    print(f"✅ {page}: Proper search structure found")
                else:
                    print(f"❌ {page}: Missing search structure")
                
                # Check for no redundant labels
                if '<label for="site-search"' not in content:
                    print(f"✅ {page}: No redundant labels")
                else:
                    print(f"❌ {page}: Redundant labels found")
                    
            except Exception as e:
                print(f"❌ {page}: Error reading file - {e}")
        else:
            print(f"⚠️  {page}: File not found")
    
    print(f"\n=== LAYOUT SUMMARY ===")
    print("Expected layout:")
    print("  - Search container: Centered with 20px left margin")
    print("  - Search title: Centered above search bar")
    print("  - Search bar: Slightly to the right of original position")
    print("  - Mobile: Full width with left-aligned title")
    
    print(f"\n=== TEST COMPLETE ===")
    print("Check your browser to see the updated search bar positioning!")

if __name__ == "__main__":
    test_search_bar_positioning()
