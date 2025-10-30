#!/usr/bin/env python3
"""
Debug Filter Button Issues

This script helps identify why specific filter buttons aren't working.
"""

import re
from datetime import datetime

def debug_filter_buttons():
    """Debug why specific filter buttons aren't working."""
    print("=== DEBUGGING FILTER BUTTON ISSUES ===")
    
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
    articles = re.findall(r'<article class="article-card"[^>]*data-category="([^"]*)"[^>]*>.*?<h3><a[^>]*>([^<]+)</a></h3>.*?<span class="article-date">([^<]+)</span>', content, re.DOTALL)
    
    print(f"\n=== ARTICLES BY CATEGORY ===")
    categories = {}
    for data_category, title, date_str in articles:
        try:
            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
        except:
            parsed_date = datetime(2025, 1, 1)
        
        if data_category not in categories:
            categories[data_category] = []
        
        categories[data_category].append({
            'title': title,
            'date': date_str,
            'parsed_date': parsed_date
        })
    
    for category, articles_list in categories.items():
        print(f"\n{category.upper()} ({len(articles_list)} articles):")
        articles_list.sort(key=lambda x: x['parsed_date'], reverse=True)
        for i, article in enumerate(articles_list, 1):
            print(f"  {i:2d}. {article['date']} - {article['title']}")
    
    # Check JavaScript
    print(f"\n=== JAVASCRIPT ANALYSIS ===")
    try:
        with open('assets/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Error reading JS file: {e}")
        return
    
    # Check for specific issues
    issues = []
    
    # Check if initCategoryFiltering is called
    if 'initCategoryFiltering()' not in js_content:
        issues.append("initCategoryFiltering() not called")
    
    # Check if event listeners are set up
    if 'addEventListener' not in js_content or 'click' not in js_content:
        issues.append("Event listeners not set up")
    
    # Check if filtering function exists
    if 'filterArticlesByCategory' not in js_content:
        issues.append("filterArticlesByCategory function missing")
    
    # Check if category comparison works
    if 'cardCategory === category' not in js_content:
        issues.append("Category comparison logic missing")
    
    # Check if DOM manipulation works
    if 'articlesGrid.innerHTML' not in js_content:
        issues.append("DOM manipulation missing")
    
    if issues:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ All JavaScript checks passed")
    
    # Test specific categories
    print(f"\n=== TESTING SPECIFIC CATEGORIES ===")
    test_categories = ['mochilas', 'carteras', 'tote-bags']
    
    for category in test_categories:
        if category in categories:
            count = len(categories[category])
            print(f"✅ {category}: {count} articles found")
        else:
            print(f"❌ {category}: No articles found")
    
    print(f"\n=== EXPECTED BEHAVIOR ===")
    print("When clicking 'Backpacks' (mochilas):")
    print(f"  - Should show {len(categories.get('mochilas', []))} articles")
    print("  - Should hide all other articles")
    print("  - Should sort by date (newest first)")
    
    print(f"\nWhen clicking 'Wallets' (carteras):")
    print(f"  - Should show {len(categories.get('carteras', []))} articles")
    print("  - Should hide all other articles")
    print("  - Should sort by date (newest first)")
    
    print(f"\nWhen clicking 'Tote Bags' (tote-bags):")
    print(f"  - Should show {len(categories.get('tote-bags', []))} articles")
    print("  - Should hide all other articles")
    print("  - Should sort by date (newest first)")

if __name__ == "__main__":
    debug_filter_buttons()
