#!/usr/bin/env python3
"""
Debug Pagination Not Updating

This script helps identify why pagination is not updating with filter buttons.
"""

import re

def debug_pagination_issue():
    """Debug why pagination is not updating."""
    print("=== DEBUGGING PAGINATION NOT UPDATING ===")
    
    try:
        with open('articles/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading articles index file: {e}")
        return
    
    # Check pagination HTML structure
    print(f"\n=== PAGINATION HTML STRUCTURE ===")
    pagination_elements = [
        'pagination-container',
        'pagination',
        'pagination-btn',
        'showing-range',
        'total-articles'
    ]
    
    for element in pagination_elements:
        if element in content:
            print(f"  ✅ {element} - found in HTML")
        else:
            print(f"  ❌ {element} - missing from HTML")
    
    # Check JavaScript for pagination functions
    print(f"\n=== JAVASCRIPT PAGINATION FUNCTIONS ===")
    try:
        with open('assets/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Error reading JS file: {e}")
        return
    
    js_functions = [
        'updatePaginationAfterFilter',
        'createPaginationControls',
        'updatePaginationInfo',
        'showPage',
        'updatePaginationButtons'
    ]
    
    for func in js_functions:
        if func in js_content:
            print(f"  ✅ {func} - found")
        else:
            print(f"  ❌ {func} - missing")
    
    # Check for the specific issue
    print(f"\n=== POTENTIAL ISSUES ===")
    
    # Check if updatePaginationInfo is using the right variable
    if 'updatePaginationInfo(startIndex + 1, endIndex, articleCards.length)' in js_content:
        print("  ✅ updatePaginationInfo using articleCards.length")
    else:
        print("  ❌ updatePaginationInfo might be using wrong variable")
    
    # Check if the pagination update is being called
    if 'updatePaginationAfterFilter(category)' in js_content:
        print("  ✅ updatePaginationAfterFilter is being called")
    else:
        print("  ❌ updatePaginationAfterFilter not being called")
    
    # Check for the total articles element update
    if 'totalArticles.textContent = total' in js_content:
        print("  ✅ totalArticles element is being updated")
    else:
        print("  ❌ totalArticles element not being updated")
    
    print(f"\n=== DEBUGGING STEPS ===")
    print("1. Open browser console")
    print("2. Click on 'Backpacks' button")
    print("3. Look for these console messages:")
    print("   - '=== FILTER CALLED ==='")
    print("   - '=== UPDATING PAGINATION ==='")
    print("   - 'Visible cards after filter: 5'")
    print("   - 'New pagination: total articles = 5 total pages = 1'")
    print("4. Check if pagination text updates to 'Showing 1-5 of 5 articles'")
    print("5. If not, there's a DOM update issue")

if __name__ == "__main__":
    debug_pagination_issue()
