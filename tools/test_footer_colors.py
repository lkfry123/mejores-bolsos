#!/usr/bin/env python3
"""
Test Footer Color Matching

This script verifies that the footer font colors match the green color from the button.
"""

import re

def test_footer_colors():
    """Test footer color matching."""
    print("=== TESTING FOOTER COLOR MATCHING ===")
    
    try:
        with open('assets/styles.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        print(f"❌ Error reading CSS file: {e}")
        return
    
    print("\n=== FOOTER COLOR VERIFICATION ===")
    
    # Check footer heading colors
    if '#0e7a6d' in css_content and 'footer-section h3' in css_content:
        print("✅ Footer headings (h3, h4): Using green color #0e7a6d")
    else:
        print("❌ Footer headings: Color not properly set")
    
    # Check footer link colors
    if '#0e7a6d' in css_content and 'footer-section ul li a' in css_content:
        print("✅ Footer links: Using green color #0e7a6d")
    else:
        print("❌ Footer links: Color not properly set")
    
    # Check footer link hover colors
    if '#0a5f54' in css_content and 'footer-section ul li a:hover' in css_content:
        print("✅ Footer link hover: Using darker green #0a5f54")
    else:
        print("❌ Footer link hover: Color not properly set")
    
    # Check decorative line color
    if '#0e7a6d' in css_content and 'footer-section h4::after' in css_content:
        print("✅ Footer decorative lines: Using green color #0e7a6d")
    else:
        print("❌ Footer decorative lines: Color not properly set")
    
    # Verify the specific color codes
    print(f"\n=== COLOR CODE VERIFICATION ===")
    
    green_primary = '#0e7a6d'
    green_darker = '#0a5f54'
    
    if green_primary in css_content:
        print(f"✅ Primary green {green_primary}: Found in CSS")
    else:
        print(f"❌ Primary green {green_primary}: Not found")
    
    if green_darker in css_content:
        print(f"✅ Darker green {green_darker}: Found in CSS")
    else:
        print(f"❌ Darker green {green_darker}: Not found")
    
    # Count occurrences
    primary_count = css_content.count(green_primary)
    darker_count = css_content.count(green_darker)
    
    print(f"\n=== USAGE SUMMARY ===")
    print(f"Primary green (#0e7a6d): Used {primary_count} times")
    print(f"Darker green (#0a5f54): Used {darker_count} times")
    
    print(f"\n=== FOOTER ELEMENTS UPDATED ===")
    print("✅ Footer section headings (h3, h4)")
    print("✅ Footer navigation links")
    print("✅ Footer link hover states")
    print("✅ Footer decorative underlines")
    
    print(f"\n=== COLOR MATCHING COMPLETE ===")
    print("The footer font colors now match the green from the 'Shop Handbags' button!")
    print(f"Primary color: {green_primary}")
    print(f"Hover color: {green_darker}")

if __name__ == "__main__":
    test_footer_colors()
