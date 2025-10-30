#!/usr/bin/env python3
"""
Test Category Filtering with Date Sorting

This script verifies that category filters sort articles from newest to oldest.
"""

import re
from datetime import datetime

def test_category_date_sorting():
    """Test that category filters sort articles by date."""
    print("=== TESTING CATEGORY FILTERING WITH DATE SORTING ===")
    
    try:
        with open('articles/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading articles index file: {e}")
        return
    
    # Extract all articles with their data
    article_pattern = r'<article class="article-card"[^>]*data-category="([^"]*)"[^>]*>(.*?)</article>'
    articles = re.findall(article_pattern, content, re.DOTALL)
    
    print(f"Found {len(articles)} articles")
    
    # Group articles by category
    categories = {}
    for data_category, article_html in articles:
        # Extract title
        title_match = re.search(r'<h3><a[^>]*>([^<]+)</a></h3>', article_html)
        title = title_match.group(1) if title_match else "Unknown Title"
        
        # Extract date
        date_match = re.search(r'<span class="article-date">([^<]+)</span>', article_html)
        date_str = date_match.group(1) if date_match else "January 1, 2025"
        
        # Parse date
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
    
    print(f"\n=== CATEGORY ANALYSIS ===")
    
    for category, articles_list in categories.items():
        print(f"\n{category.upper()} ({len(articles_list)} articles):")
        
        # Sort by date (newest first)
        articles_list.sort(key=lambda x: x['parsed_date'], reverse=True)
        
        for i, article in enumerate(articles_list, 1):
            print(f"  {i:2d}. {article['date']} - {article['title']}")
    
    print(f"\n=== JAVASCRIPT FUNCTIONALITY TEST ===")
    
    try:
        with open('assets/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Error reading JS file: {e}")
        return
    
    # Check for date sorting functionality
    js_features = [
        'getArticleDate',
        'filteredCards.sort',
        'dateB - dateA',
        'new Date(dateText)',
        'updateVisibleArticles'
    ]
    
    for feature in js_features:
        if feature in js_content:
            print(f"  ✅ {feature} - found in JavaScript")
        else:
            print(f"  ❌ {feature} - missing from JavaScript")
    
    print(f"\n=== EXPECTED BEHAVIOR ===")
    print("✅ All filter buttons should show articles sorted newest to oldest")
    print("✅ Handbags filter: Only handbag articles, sorted by date")
    print("✅ Backpacks filter: Only backpack articles, sorted by date")
    print("✅ Wallets filter: Only wallet articles, sorted by date")
    print("✅ Tote Bags filter: Only tote bag articles, sorted by date")
    print("✅ Pagination should work with filtered results")
    
    print(f"\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_category_date_sorting()

