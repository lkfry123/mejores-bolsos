#!/usr/bin/env python3
"""
Debug Category Filtering

This script helps debug why category filtering isn't working properly.
"""

import re

def debug_category_filtering():
    """Debug the category filtering issue."""
    print("=== DEBUGGING CATEGORY FILTERING ===")
    
    try:
        with open('articles/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading articles index file: {e}")
        return
    
    # Extract filter buttons
    filter_buttons = re.findall(r'<button class="filter-btn"[^>]*data-category="([^"]*)"[^>]*>([^<]+)</button>', content)
    print(f"\n=== FILTER BUTTONS ===")
    for category, text in filter_buttons:
        print(f"  {text}: data-category='{category}'")
    
    # Extract articles and their categories
    articles = re.findall(r'<article class="article-card"[^>]*data-category="([^"]*)"[^>]*>.*?<h3><a[^>]*>([^<]+)</a></h3>', content, re.DOTALL)
    print(f"\n=== ARTICLES BY CATEGORY ===")
    
    categories = {}
    for category, title in articles:
        if category not in categories:
            categories[category] = []
        categories[category].append(title)
    
    for category, articles_list in categories.items():
        print(f"\n{category.upper()} ({len(articles_list)} articles):")
        for i, title in enumerate(articles_list, 1):
            print(f"  {i:2d}. {title}")
    
    # Check for JavaScript issues
    print(f"\n=== JAVASCRIPT ANALYSIS ===")
    try:
        with open('assets/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Error reading JS file: {e}")
        return
    
    # Check for filtering logic
    if 'cardCategory === category' in js_content:
        print("  ✅ Category comparison logic found")
    else:
        print("  ❌ Category comparison logic missing")
    
    if 'data-category' in js_content:
        print("  ✅ data-category attribute access found")
    else:
        print("  ❌ data-category attribute access missing")
    
    if 'filteredCards.push(card)' in js_content:
        print("  ✅ Article filtering logic found")
    else:
        print("  ❌ Article filtering logic missing")
    
    # Check for event listeners
    if 'addEventListener' in js_content and 'click' in js_content:
        print("  ✅ Click event listeners found")
    else:
        print("  ❌ Click event listeners missing")
    
    print(f"\n=== EXPECTED BEHAVIOR ===")
    print("When clicking 'Handbags' button:")
    print(f"  - Should show {len(categories.get('bolsos-de-mano', []))} handbag articles")
    print("  - Should hide all other articles")
    print("  - Should sort by date (newest first)")
    
    print(f"\nWhen clicking 'Backpacks' button:")
    print(f"  - Should show {len(categories.get('mochilas', []))} backpack articles")
    print("  - Should hide all other articles")
    print("  - Should sort by date (newest first)")
    
    print(f"\n=== DEBUGGING COMPLETE ===")

if __name__ == "__main__":
    debug_category_filtering()