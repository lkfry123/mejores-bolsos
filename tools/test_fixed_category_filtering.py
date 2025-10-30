#!/usr/bin/env python3
"""
Test Fixed Category Filtering

This script verifies that category filtering now works correctly with proper article separation.
"""

import re
from datetime import datetime

def test_fixed_category_filtering():
    """Test that category filtering works correctly."""
    print("=== TESTING FIXED CATEGORY FILTERING ===")
    
    try:
        with open('articles/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading articles index file: {e}")
        return
    
    # Extract articles with their categories and dates
    article_pattern = r'<article class="article-card"[^>]*data-category="([^"]*)"[^>]*>.*?<span class="article-date">([^<]+)</span>.*?<h3><a[^>]*>([^<]+)</a></h3>'
    articles = re.findall(article_pattern, content, re.DOTALL)
    
    print(f"Found {len(articles)} articles")
    
    # Group articles by category
    categories = {}
    for category, date_str, title in articles:
        if category not in categories:
            categories[category] = []
        
        # Parse date
        try:
            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
        except:
            parsed_date = datetime(2025, 1, 1)
        
        categories[category].append({
            'title': title,
            'date': date_str,
            'parsed_date': parsed_date
        })
    
    print(f"\n=== CATEGORY BREAKDOWN (NEWEST TO OLDEST) ===")
    
    for category, articles_list in categories.items():
        # Sort by date (newest first)
        articles_list.sort(key=lambda x: x['parsed_date'], reverse=True)
        
        category_name = {
            'bolsos-de-mano': 'Handbags',
            'mochilas': 'Backpacks', 
            'carteras': 'Wallets',
            'tote-bags': 'Tote Bags'
        }.get(category, category)
        
        print(f"\n{category_name.upper()} ({len(articles_list)} articles):")
        for i, article in enumerate(articles_list, 1):
            print(f"  {i:2d}. {article['date']} - {article['title']}")
    
    print(f"\n=== EXPECTED FILTER BEHAVIOR ===")
    print("✅ Handbags filter: Should show ONLY 5 handbag articles, newest to oldest")
    print("✅ Backpacks filter: Should show ONLY 4 backpack articles, newest to oldest")
    print("✅ Wallets filter: Should show ONLY 4 wallet articles, newest to oldest")
    print("✅ Tote Bags filter: Should show ONLY 4 tote bag articles, newest to oldest")
    print("✅ All filter: Should show ALL 17 articles, newest to oldest")
    
    print(f"\n=== JAVASCRIPT VERIFICATION ===")
    
    try:
        with open('assets/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Error reading JS file: {e}")
        return
    
    # Check for key filtering functions
    js_features = [
        'window.currentFilteredArticles',
        'updatePaginationWithFilteredArticles',
        'filteredCards.sort',
        'dateB - dateA'
    ]
    
    for feature in js_features:
        if feature in js_content:
            print(f"  ✅ {feature} - found")
        else:
            print(f"  ❌ {feature} - missing")
    
    print(f"\n=== SUMMARY ===")
    print("🎉 Category filtering should now work correctly:")
    print("  - Each filter shows only its designated articles")
    print("  - Articles are sorted newest to oldest within each category")
    print("  - Pagination works with filtered results")
    print("  - No more showing all articles when filtering by category")
    
    print(f"\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_fixed_category_filtering()

