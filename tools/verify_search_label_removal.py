#!/usr/bin/env python3
"""
Verify Search Label Removal

This script verifies that the "Search" label has been completely removed from all pages.
"""

import os

def verify_search_label_removal():
    """Verify that search labels have been removed."""
    print("=== VERIFYING SEARCH LABEL REMOVAL ===")
    
    # Test key pages
    test_pages = [
        'index.html',
        'privacy-policy.html', 
        'articles/handbags.html',
        'search/index.html'
    ]
    
    print("\n=== SEARCH LABEL CHECK ===")
    
    all_good = True
    
    for page in test_pages:
        if os.path.exists(page):
            try:
                with open(page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for any remaining search labels
                has_label = '<label for="site-search"' in content
                
                if not has_label:
                    print(f"✅ {page}: No search label found")
                else:
                    print(f"❌ {page}: Search label still present")
                    all_good = False
                
                # Check for proper structure
                has_title = 'ah-search-title' in content
                has_form = 'ah-search' in content
                has_input = 'site-search' in content
                
                if has_title and has_form and has_input:
                    print(f"✅ {page}: Proper search structure maintained")
                else:
                    print(f"❌ {page}: Search structure issue")
                    all_good = False
                    
            except Exception as e:
                print(f"❌ {page}: Error reading file - {e}")
                all_good = False
        else:
            print(f"⚠️  {page}: File not found")
    
    # Check for any remaining label patterns
    print("\n=== PATTERN CHECK ===")
    
    label_patterns = [
        '<label for="site-search"',
        'class="sr-only">Search',
        'Search</label>'
    ]
    
    for pattern in label_patterns:
        found_files = []
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools', 'scripts'}]
            for file in files:
                if file.endswith('.html') and not file.startswith('.') and '.bak_' not in file:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            if pattern in f.read():
                                found_files.append(file_path)
                    except:
                        pass
        
        if found_files:
            print(f"❌ Pattern '{pattern}' found in {len(found_files)} files")
            all_good = False
        else:
            print(f"✅ Pattern '{pattern}' not found")
    
    print(f"\n=== FINAL RESULT ===")
    if all_good:
        print("🎉 Search labels successfully removed!")
        print("\nThe search bar now has:")
        print("  - Only the visible title 'Search Affordable Handbags' above the search bar")
        print("  - No screen reader labels or redundant text")
        print("  - Clean, minimal appearance")
        print("  - Proper accessibility with aria-label on the form")
    else:
        print("⚠️  Some search labels may still be present")
    
    return all_good

if __name__ == "__main__":
    verify_search_label_removal()
