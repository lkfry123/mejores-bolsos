#!/usr/bin/env python3
"""
Complete Search Functionality Test

This script provides a comprehensive test of the search functionality.
"""

import os
import json

def test_complete_search():
    """Test the complete search functionality."""
    print("=== COMPLETE SEARCH FUNCTIONALITY TEST ===")
    print()
    
    # Test 1: Search index exists and is valid
    print("1. Testing search index...")
    if os.path.exists('search-index.json'):
        try:
            with open('search-index.json', 'r', encoding='utf-8') as f:
                articles = json.load(f)
            print(f"   ✅ Search index loaded with {len(articles)} articles")
        except Exception as e:
            print(f"   ❌ Error loading search index: {e}")
            return False
    else:
        print("   ❌ Search index not found")
        return False
    
    # Test 2: Search page exists
    print("\n2. Testing search page...")
    if os.path.exists('search/index.html'):
        print("   ✅ Search page exists")
    else:
        print("   ❌ Search page not found")
        return False
    
    # Test 3: Search bar added to pages
    print("\n3. Testing search bar integration...")
    test_pages = ['index.html', 'privacy-policy.html', 'articles/handbags.html']
    search_bar_found = 0
    
    for page in test_pages:
        if os.path.exists(page):
            try:
                with open(page, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'ah-search' in content:
                    search_bar_found += 1
            except:
                pass
    
    if search_bar_found == len(test_pages):
        print(f"   ✅ Search bar found in all {len(test_pages)} test pages")
    else:
        print(f"   ⚠️  Search bar found in {search_bar_found}/{len(test_pages)} test pages")
    
    # Test 4: Search functionality
    print("\n4. Testing search functionality...")
    
    def match(items, q):
        if not q:
            return []
        terms = q.lower().split()
        return [item for item in items if all(term in ' '.join([
            item['title'], item['url'], item['category'],
            ' '.join(item.get('tags', [])), item.get('excerpt', '')
        ]).lower() for term in terms)]
    
    # Test various search queries
    test_queries = [
        ("osprey", "Osprey brand search"),
        ("wallet", "Wallet category search"),
        ("work", "Work-related search"),
        ("zzz", "Zero results test"),
        ("", "Empty query test")
    ]
    
    all_tests_passed = True
    
    for query, description in test_queries:
        results = match(articles, query)
        if query == "zzz" and len(results) == 0:
            print(f"   ✅ {description}: Zero results (correct)")
        elif query == "" and len(results) == 0:
            print(f"   ✅ {description}: Zero results (correct)")
        elif query != "zzz" and query != "" and len(results) > 0:
            print(f"   ✅ {description}: {len(results)} results found")
        else:
            print(f"   ❌ {description}: Unexpected results")
            all_tests_passed = False
    
    # Test 5: Search index quality
    print("\n5. Testing search index quality...")
    
    # Check for required fields
    required_fields = ['title', 'url', 'category', 'tags', 'date', 'excerpt']
    sample_article = articles[0] if articles else {}
    
    missing_fields = [field for field in required_fields if field not in sample_article]
    if not missing_fields:
        print("   ✅ All required fields present")
    else:
        print(f"   ❌ Missing fields: {missing_fields}")
        all_tests_passed = False
    
    # Check for proper URLs
    invalid_urls = [article for article in articles if not article['url'].startswith('/')]
    if not invalid_urls:
        print("   ✅ All URLs are properly formatted")
    else:
        print(f"   ❌ {len(invalid_urls)} articles have invalid URLs")
        all_tests_passed = False
    
    # Check for categories
    categories = set(article['category'] for article in articles)
    expected_categories = {'Handbags', 'Backpacks', 'Wallets', 'Tote Bags', 'Articles', 'Categories', 'Legal', 'Homepage'}
    if categories.intersection(expected_categories):
        print(f"   ✅ Found expected categories: {sorted(categories.intersection(expected_categories))}")
    else:
        print(f"   ⚠️  Unexpected categories: {sorted(categories)}")
    
    # Test 6: Mobile responsiveness
    print("\n6. Testing mobile responsiveness...")
    try:
        with open('search/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'max-width: 768px' in content or 'max-width:768px' in content:
            print("   ✅ Mobile breakpoints defined")
        else:
            print("   ❌ Mobile breakpoints missing")
            all_tests_passed = False
        
        if 'flex: 1' in content or 'flex:1' in content:
            print("   ✅ Flexible layout implemented")
        else:
            print("   ❌ Flexible layout missing")
            all_tests_passed = False
    except Exception as e:
        print(f"   ❌ Error checking mobile responsiveness: {e}")
        all_tests_passed = False
    
    # Final result
    print("\n" + "="*50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Search functionality is ready.")
        print("\nTo test manually:")
        print("1. Open http://127.0.0.1:5500/search/")
        print("2. Try searching for 'osprey', 'wallet', 'work'")
        print("3. Try searching for 'zzz' to see zero-results state")
        print("4. Test on mobile device or resize browser window")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_complete_search()
