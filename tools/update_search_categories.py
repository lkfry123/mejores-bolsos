#!/usr/bin/env python3
"""
Update Search Index Categories

This script updates the search index with better category detection.
"""

import json
import re

def update_categories():
    """Update categories in the search index."""
    try:
        with open('search-index.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"❌ Error reading search-index.json: {e}")
        return
    
    updated_count = 0
    
    for article in articles:
        url = article['url']
        title = article['title']
        
        # Better category detection
        if '/articles/handbags' in url or 'handbag' in title.lower():
            article['category'] = 'Handbags'
            updated_count += 1
        elif '/articles/backpacks' in url or 'backpack' in title.lower():
            article['category'] = 'Backpacks'
            updated_count += 1
        elif '/articles/wallets' in url or 'wallet' in title.lower():
            article['category'] = 'Wallets'
            updated_count += 1
        elif '/articles/tote-bags' in url or 'tote' in title.lower():
            article['category'] = 'Tote Bags'
            updated_count += 1
        elif '/categories/handbags' in url or 'bolsos de mano' in title.lower():
            article['category'] = 'Handbags'
            updated_count += 1
        elif '/categories/backpacks' in url or 'mochilas' in title.lower():
            article['category'] = 'Backpacks'
            updated_count += 1
        elif '/categories/wallets' in url or 'carteras' in title.lower():
            article['category'] = 'Wallets'
            updated_count += 1
        elif '/categories/tote-bags' in url:
            article['category'] = 'Tote Bags'
            updated_count += 1
        elif 'privacy' in title.lower():
            article['category'] = 'Legal'
        elif 'affiliate' in title.lower():
            article['category'] = 'Legal'
        elif 'index' in url and 'articles' in url:
            article['category'] = 'Articles'
        elif 'index' in url and 'categories' in url:
            article['category'] = 'Categories'
        elif 'index' in url and url == '/index.html':
            article['category'] = 'Homepage'
    
    # Write updated JSON
    try:
        with open('search-index.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated {updated_count} categories in search-index.json")
    except Exception as e:
        print(f"❌ Error writing search-index.json: {e}")

if __name__ == "__main__":
    update_categories()
