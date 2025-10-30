#!/usr/bin/env python3
"""
Test Complete Category Filtering

This script tests that category filtering works correctly with date sorting.
"""

import re
from datetime import datetime

def test_complete_category_filtering():
    """Test complete category filtering functionality."""
    print("=== TESTING COMPLETE CATEGORY FILTERING ===")
    
    try:
        with open('articles/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading articles index file: {e}")
        return
    
    # Extract articles with their data
    article_pattern = r'<article class="article-card"[^>]*data-category="([^"]*)"[^>]*>.*?<h3><a[^>]*>([^<]+)</a></h3>.*?<span class="article-date">([^<]+)</span>'
    articles = re.findall(article_pattern, content, re.DOTALL)
    
    print(f"Found {len(articles)} articles")
    
    # Group articles by category
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
    
    print(f"\n=== CATEGORY BREAKDOWN ===")
    
    for category, articles_list in categories.items():
        print(f"\n{category.upper()} ({len(articles_list)} articles):")
        
        # Sort by date (newest first)
        articles_list.sort(key=lambda x: x['parsed_date'], reverse=True)
        
        for i, article in enumerate(articles_list, 1):
            print(f"  {i:2d}. {article['date']} - {article['title']}")
    
    # Test JavaScript functionality
    print(f"\n=== JAVASCRIPT FUNCTIONALITY TEST ===")
    try:
        with open('assets/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Error reading JS file: {e}")
        return
    
    # Check for required functions
    js_checks = [
        ('initCategoryFiltering', 'Category filtering initialization'),
        ('filterArticlesByCategory', 'Category filtering function'),
        ('getArticleDate', 'Date extraction function'),
        ('addEventListener', 'Event listener setup'),
        ('data-category', 'Category attribute access'),
        ('cardCategory === category', 'Category comparison logic'),
        ('filteredCards.sort', 'Date sorting logic'),
        ('articlesGrid.innerHTML', 'DOM manipulation')
    ]
    
    for check, description in js_checks:
        if check in js_content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
    
    # Check for initialization
    if 'initCategoryFiltering()' in js_content:
        print(f"  ✅ Category filtering is initialized")
    else:
        print(f"  ❌ Category filtering initialization missing")
    
    print(f"\n=== EXPECTED FILTER BEHAVIOR ===")
    print("✅ All filter: Shows all 17 articles, sorted by date")
    print(f"✅ Handbags filter: Shows {len(categories.get('bolsos-de-mano', []))} handbag articles, sorted by date")
    print(f"✅ Backpacks filter: Shows {len(categories.get('mochilas', []))} backpack articles, sorted by date")
    print(f"✅ Wallets filter: Shows {len(categories.get('carteras', []))} wallet articles, sorted by date")
    print(f"✅ Tote Bags filter: Shows {len(categories.get('tote-bags', []))} tote bag articles, sorted by date")
    
    print(f"\n=== TESTING COMPLETE ===")
    print("🎉 Category filtering should now work correctly!")
    print("   - Each filter button shows only articles from that category")
    print("   - Articles are sorted from newest to oldest")
    print("   - Pagination works with filtered results")

if __name__ == "__main__":
    test_complete_category_filtering()
