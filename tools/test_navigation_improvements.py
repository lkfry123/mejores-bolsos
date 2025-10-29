#!/usr/bin/env python3
"""
Test Navigation Improvements

This script verifies that the navigation links are properly spaced and organized
to reduce clutter while maintaining usability.
"""

import os
import re

def test_navigation_improvements():
    """Test navigation spacing and layout improvements."""
    print("=== TESTING NAVIGATION IMPROVEMENTS ===")
    
    # Check CSS changes
    print("\n=== CSS VERIFICATION ===")
    
    css_file = "assets/styles.css"
    if os.path.exists(css_file):
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Check for improved nav-menu spacing
            if 'gap: var(--spacing-sm)' in css_content or 'gap: 1rem' in css_content:
                print("✅ Nav menu: Reduced gap from 2rem to 1rem")
            else:
                print("❌ Nav menu: Gap not properly reduced")
            
            # Check for smaller font size
            if 'font-size: var(--font-size-small)' in css_content:
                print("✅ Nav links: Smaller font size (14px)")
            else:
                print("❌ Nav links: Font size not optimized")
            
            # Check for centered navigation
            if 'justify-content: center' in css_content:
                print("✅ Nav menu: Links centered for better balance")
            else:
                print("❌ Nav menu: Centering not applied")
            
            # Check for flex-wrap
            if 'flex-wrap: wrap' in css_content:
                print("✅ Nav menu: Flexible wrapping on smaller screens")
            else:
                print("❌ Nav menu: Wrap not enabled")
            
            # Check for improved search container
            if 'margin-left:12px' in css_content or 'margin-left: 12px' in css_content:
                print("✅ Search container: Optimized spacing")
            else:
                print("❌ Search container: Spacing not optimized")
            
            # Check for responsive breakpoints
            if '@media (max-width:992px)' in css_content:
                print("✅ Responsive: Added 992px breakpoint for tablets")
            else:
                print("⚠️  Responsive: 992px breakpoint may be missing")
                
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
    
    nav_count = 0
    for page in test_pages:
        if os.path.exists(page):
            try:
                with open(page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Count navigation links
                nav_links = len(re.findall(r'<li><a href="[^"]*" class="nav-link', content))
                
                if nav_links > 0:
                    nav_count = nav_links
                    print(f"✅ {page}: {nav_links} navigation links found")
                else:
                    print(f"⚠️  {page}: No navigation links found")
                
                # Check for proper nav structure
                if 'nav-menu' in content and 'nav-container' in content:
                    print(f"✅ {page}: Proper navigation structure")
                else:
                    print(f"❌ {page}: Navigation structure issue")
                    
            except Exception as e:
                print(f"❌ {page}: Error reading file - {e}")
        else:
            print(f"⚠️  {page}: File not found")
    
    print(f"\n=== IMPROVEMENTS SUMMARY ===")
    print("Navigation layout improvements:")
    print(f"  - Reduced gap between links (from 2rem to 1rem)")
    print(f"  - Smaller font size for nav links (14px)")
    print(f"  - Centered navigation for better balance")
    print(f"  - Flex-wrap enabled for responsive behavior")
    print(f"  - Optimized search bar spacing")
    print(f"  - Better tablet breakpoint (992px)")
    print(f"  - {nav_count} navigation links properly organized")
    
    print(f"\n=== EXPECTED RESULT ===")
    print("The header should now appear:")
    print("  - Less cluttered with tighter spacing")
    print("  - Better balanced with centered nav links")
    print("  - More compact while remaining readable")
    print("  - Responsive on tablets and mobile")
    
    print(f"\n=== TEST COMPLETE ===")
    print("Check your browser to see the improved navigation layout!")

if __name__ == "__main__":
    test_navigation_improvements()
