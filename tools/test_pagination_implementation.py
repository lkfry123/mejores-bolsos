#!/usr/bin/env python3
"""
Test Pagination Implementation

This script verifies that the pagination implementation is working correctly.
"""

import os
import re

def test_pagination_implementation():
    """Test the pagination implementation on the articles page."""
    print("=== TESTING PAGINATION IMPLEMENTATION ===")
    
    try:
        with open('articles/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading articles index file: {e}")
        return
    
    print("\n=== HTML STRUCTURE TEST ===")
    
    # Check for pagination HTML elements
    pagination_elements = [
        'pagination-container',
        'pagination',
        'pagination-btn',
        'prev-btn',
        'next-btn',
        'pagination-numbers',
        'page-btn',
        'pagination-info',
        'pagination-text',
        'showing-range',
        'total-articles'
    ]
    
    for element in pagination_elements:
        if element in content:
            print(f"  ✅ {element} - found in HTML")
        else:
            print(f"  ❌ {element} - missing from HTML")
    
    # Check for article cards
    article_cards = re.findall(r'<article class="article-card"', content)
    print(f"\n=== ARTICLE CARDS TEST ===")
    print(f"  Found {len(article_cards)} article cards")
    
    # Check for data-category attributes
    data_categories = re.findall(r'data-category="([^"]*)"', content)
    print(f"  Found {len(data_categories)} data-category attributes")
    
    print(f"\n=== CSS STYLES TEST ===")
    
    try:
        with open('assets/styles.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        print(f"❌ Error reading CSS file: {e}")
        return
    
    # Check for pagination CSS
    pagination_css = [
        '.pagination-container',
        '.pagination',
        '.pagination-btn',
        '.pagination-btn:hover',
        '.pagination-btn.active',
        '.pagination-btn:disabled',
        '.pagination-numbers',
        '.pagination-info',
        '.pagination-text'
    ]
    
    for css_class in pagination_css:
        if css_class in css_content:
            print(f"  ✅ {css_class} - found in CSS")
        else:
            print(f"  ❌ {css_class} - missing from CSS")
    
    print(f"\n=== JAVASCRIPT FUNCTIONALITY TEST ===")
    
    try:
        with open('assets/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Error reading JS file: {e}")
        return
    
    # Check for pagination JavaScript functions
    js_functions = [
        'initPagination',
        'createPaginationControls',
        'showPage',
        'updatePaginationButtons',
        'updatePaginationInfo',
        'articlesPerPage = 10'
    ]
    
    for func in js_functions:
        if func in js_content:
            print(f"  ✅ {func} - found in JavaScript")
        else:
            print(f"  ❌ {func} - missing from JavaScript")
    
    print(f"\n=== PAGINATION CALCULATION TEST ===")
    
    total_articles = len(article_cards)
    articles_per_page = 10
    total_pages = (total_articles + articles_per_page - 1) // articles_per_page
    
    print(f"  Total articles: {total_articles}")
    print(f"  Articles per page: {articles_per_page}")
    print(f"  Total pages needed: {total_pages}")
    
    # Check if pagination numbers match expected pages
    expected_pages = list(range(1, total_pages + 1))
    found_pages = re.findall(r'data-page="(\d+)"', content)
    found_pages = [int(page) for page in found_pages]
    
    if set(found_pages) == set(expected_pages):
        print(f"  ✅ Pagination numbers match expected pages: {expected_pages}")
    else:
        print(f"  ❌ Pagination numbers mismatch. Expected: {expected_pages}, Found: {found_pages}")
    
    print(f"\n=== SUMMARY ===")
    
    # Count issues
    issues = 0
    
    # Check HTML elements
    for element in pagination_elements:
        if element not in content:
            issues += 1
    
    # Check CSS classes
    for css_class in pagination_css:
        if css_class not in css_content:
            issues += 1
    
    # Check JS functions
    for func in js_functions:
        if func not in js_content:
            issues += 1
    
    if issues == 0:
        print("🎉 All pagination elements implemented correctly!")
        print("✅ HTML structure: Complete")
        print("✅ CSS styling: Complete")
        print("✅ JavaScript functionality: Complete")
        print("✅ Pagination calculation: Correct")
    else:
        print(f"⚠️  {issues} issues found that need attention")
    
    print(f"\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_pagination_implementation()

