#!/usr/bin/env python3
"""
Enhanced Search Functionality

This script improves the search functionality with better matching, ranking, and suggestions.
"""

import json
import re
from difflib import SequenceMatcher

def enhanced_search(items, query):
    """Enhanced search with better matching and ranking."""
    if not query:
        return []
    
    query_lower = query.lower().strip()
    terms = [t for t in query_lower.split() if t]
    
    if not terms:
        return []
    
    results = []
    
    for item in items:
        # Build searchable content
        content_parts = [
            item.get('title', ''),
            item.get('category', ''),
            ' '.join(item.get('tags', [])),
            item.get('excerpt', '')
        ]
        content = ' '.join(content_parts).lower()
        
        # Calculate relevance score
        score = 0
        matches = []
        
        # Exact phrase match (highest priority)
        if query_lower in content:
            score += 100
            matches.append(f"Exact phrase: '{query_lower}'")
        
        # Title match (high priority)
        title = item.get('title', '').lower()
        if query_lower in title:
            score += 50
            matches.append("Title match")
        
        # Individual term matches
        term_matches = 0
        for term in terms:
            if term in content:
                term_matches += 1
                # Boost score for title matches
                if term in title:
                    score += 20
                else:
                    score += 10
        
        # All terms must be present
        if term_matches == len(terms):
            # Bonus for matching all terms
            score += 30
            
            # Add fuzzy matching for typos
            for term in terms:
                best_ratio = 0
                for word in content.split():
                    ratio = SequenceMatcher(None, term, word).ratio()
                    if ratio > 0.8:  # 80% similarity
                        best_ratio = max(best_ratio, ratio)
                
                if best_ratio > 0.8:
                    score += int(best_ratio * 10)
                    matches.append(f"Fuzzy match: {best_ratio:.2f}")
        
        if score > 0:
            results.append({
                'item': item,
                'score': score,
                'matches': matches
            })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return [r['item'] for r in results]

def test_enhanced_search():
    """Test the enhanced search functionality."""
    print("=== TESTING ENHANCED SEARCH ===")
    
    # Load search index
    try:
        with open('search-index.json', 'r', encoding='utf-8') as f:
            index = json.load(f)
        print(f"✅ Loaded search index with {len(index)} items")
    except Exception as e:
        print(f"❌ Error loading search index: {e}")
        return
    
    # Test various search queries
    test_queries = [
        "Osprey",
        "osprey women",
        "osprey backpack",
        "hiking backpack",
        "travel bag",
        "wallet",
        "crossbody",
        "work tote",
        "laptop bag"
    ]
    
    for query in test_queries:
        print(f"\n=== SEARCHING FOR: '{query}' ===")
        results = enhanced_search(index, query)
        print(f"Found {len(results)} results:")
        
        for i, result in enumerate(results[:5], 1):  # Show top 5
            print(f"  {i}. {result.get('title', 'No title')}")
            print(f"     URL: {result.get('url', 'No URL')}")
            print(f"     Category: {result.get('category', 'No category')}")
            print(f"     Tags: {', '.join(result.get('tags', [])[:5])}")
            print()
    
    print("=== ENHANCED SEARCH TEST COMPLETE ===")

if __name__ == "__main__":
    test_enhanced_search()
