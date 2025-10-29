#!/usr/bin/env python3
"""
Test Search Functionality

This script tests the search functionality to see why "Osprey" isn't being found.
"""

import json
import re

def test_search_function():
    """Test the search matching logic."""
    print("=== TESTING SEARCH FUNCTIONALITY ===")
    
    # Load search index
    try:
        with open('search-index.json', 'r', encoding='utf-8') as f:
            index = json.load(f)
        print(f"✅ Loaded search index with {len(index)} items")
    except Exception as e:
        print(f"❌ Error loading search index: {e}")
        return
    
    # Test search function (replicating JavaScript logic)
    def match(items, q):
        if not q:
            return []
        
        terms = q.lower().split()
        terms = [t for t in terms if t]  # filter(Boolean)
        
        results = []
        for it in items:
            hay = ' '.join([
                it.get('title', ''),
                it.get('url', ''),
                it.get('category', ''),
                ' '.join(it.get('tags', [])),
                it.get('excerpt', '')
            ]).lower()
            
            # Check if all terms are found
            if all(term in hay for term in terms):
                results.append(it)
        
        return results
    
    # Test "Osprey" search
    print("\n=== TESTING 'OSPREY' SEARCH ===")
    osprey_results = match(index, "Osprey")
    print(f"Found {len(osprey_results)} results for 'Osprey':")
    
    for i, result in enumerate(osprey_results, 1):
        print(f"  {i}. {result.get('title', 'No title')}")
        print(f"     URL: {result.get('url', 'No URL')}")
        print(f"     Tags: {', '.join(result.get('tags', []))}")
        print()
    
    # Test case sensitivity
    print("=== TESTING CASE SENSITIVITY ===")
    osprey_lower = match(index, "osprey")
    print(f"Found {len(osprey_lower)} results for 'osprey' (lowercase)")
    
    # Test partial matches
    print("\n=== TESTING PARTIAL MATCHES ===")
    osp_partial = match(index, "osp")
    print(f"Found {len(osp_partial)} results for 'osp' (partial)")
    
    # Check what content actually contains "osprey"
    print("\n=== CONTENT ANALYSIS ===")
    osprey_items = []
    for item in index:
        content = ' '.join([
            item.get('title', ''),
            item.get('url', ''),
            item.get('category', ''),
            ' '.join(item.get('tags', [])),
            item.get('excerpt', '')
        ]).lower()
        
        if 'osprey' in content:
            osprey_items.append({
                'title': item.get('title', ''),
                'url': item.get('url', ''),
                'content_snippet': content[:200] + '...' if len(content) > 200 else content
            })
    
    print(f"Items containing 'osprey' in content: {len(osprey_items)}")
    for item in osprey_items:
        print(f"  - {item['title']}")
        print(f"    Content: {item['content_snippet']}")
        print()
    
    # Test other search terms
    print("\n=== TESTING OTHER SEARCH TERMS ===")
    test_terms = ["backpack", "hiking", "travel", "wallet"]
    for term in test_terms:
        results = match(index, term)
        print(f"'{term}': {len(results)} results")
    
    print("\n=== SEARCH ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    test_search_function()
