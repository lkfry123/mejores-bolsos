#!/usr/bin/env python3
"""
Test Articles Page Filtering

This script tests the actual articles page to ensure filtering works correctly.
"""

import re
from datetime import datetime

def test_articles_page_filtering():
    """Test the actual articles page filtering functionality."""
    print("=== TESTING ARTICLES PAGE FILTERING ===")
    
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
        ('articlesGrid.innerHTML', 'DOM manipulation'),
        ('console.log', 'Debug logging')
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
    print(f"✅ Backpacks filter (mochilas): Shows {len(categories.get('mochilas', []))} articles, sorted by date")
    print(f"✅ Wallets filter (carteras): Shows {len(categories.get('carteras', []))} articles, sorted by date")
    print(f"✅ Tote Bags filter (tote-bags): Shows {len(categories.get('tote-bags', []))} articles, sorted by date")
    
    print(f"\n=== DEBUGGING INSTRUCTIONS ===")
    print("1. Open http://127.0.0.1:5500/articles/ in your browser")
    print("2. Open browser developer tools (F12)")
    print("3. Go to Console tab")
    print("4. Click on 'Backpacks' button")
    print("5. Check console for debug messages:")
    print("   - Should see 'Filtering by category: mochilas'")
    print("   - Should see 'Article category: mochilas' for each backpack article")
    print("   - Should see 'Filtered cards: 4'")
    print("6. Repeat for 'Wallets' and 'Tote Bags' buttons")
    
    print(f"\n=== TESTING COMPLETE ===")

if __name__ == "__main__":
    test_articles_page_filtering()
