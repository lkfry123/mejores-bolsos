#!/usr/bin/env python3
"""
Test Search Functionality

This script tests the search functionality by simulating searches.
"""

import json
import os

def test_search():
    """Test search functionality."""
    print("=== TESTING SEARCH FUNCTIONALITY ===")
    
    # Load search index
    try:
        with open('search-index.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        print(f"✅ Loaded {len(articles)} articles from search index")
    except Exception as e:
        print(f"❌ Error loading search index: {e}")
        return
    
    # Test search function
    def match(items, q):
        if not q:
            return []
        terms = q.lower().split()
        return [item for item in items if all(term in ' '.join([
            item['title'], item['url'], item['category'],
            ' '.join(item.get('tags', [])), item.get('excerpt', '')
        ]).lower() for term in terms)]
    
    # Test cases
    test_cases = [
        ("osprey", "Should find Osprey articles"),
        ("wallet", "Should find wallet articles"),
        ("backpack", "Should find backpack articles"),
        ("handbag", "Should find handbag articles"),
        ("zzz", "Should return no results (zero state)"),
        ("", "Should return no results (empty query)"),
        ("work", "Should find work-related articles"),
        ("affordable", "Should find affordable articles")
    ]
    
    print("\n=== SEARCH TESTS ===")
    
    for query, description in test_cases:
        results = match(articles, query)
        print(f"\nQuery: '{query}' - {description}")
        print(f"Results: {len(results)}")
        
        if results:
            for i, result in enumerate(results[:3]):  # Show first 3 results
                print(f"  {i+1}. {result['title']} ({result['category']})")
        else:
            print("  No results found")
    
    # Test zero-results suggestions
    print("\n=== ZERO-RESULTS SUGGESTIONS ===")
    no_results = match(articles, "zzz")
    if not no_results:
        print("✅ Zero-results state would show suggestions")
        print("  - Popular categories")
        print("  - Latest articles")
        print("  - Quick tips")
    else:
        print("❌ Zero-results test failed")
    
    # Test search index structure
    print("\n=== SEARCH INDEX STRUCTURE ===")
    if articles:
        sample = articles[0]
        required_fields = ['title', 'url', 'category', 'tags', 'date', 'excerpt']
        missing_fields = [field for field in required_fields if field not in sample]
        
        if not missing_fields:
            print("✅ All required fields present")
        else:
            print(f"❌ Missing fields: {missing_fields}")
        
        print(f"Sample entry:")
        print(f"  Title: {sample['title']}")
        print(f"  URL: {sample['url']}")
        print(f"  Category: {sample['category']}")
        print(f"  Tags: {sample['tags'][:5]}...")  # First 5 tags
        print(f"  Date: {sample['date']}")
        print(f"  Excerpt: {sample['excerpt'][:100]}...")  # First 100 chars

if __name__ == "__main__":
    test_search()
