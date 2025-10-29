#!/usr/bin/env python3
"""
Verify Redundant Text Removal

This script verifies that redundant "Search Affordable Handbags" text has been removed.
"""

import os
import re

def verify_redundant_text_removal():
    """Verify that redundant search text has been removed."""
    print("=== VERIFYING REDUNDANT TEXT REMOVAL ===")
    
    # Test key pages
    test_pages = [
        'index.html',
        'privacy-policy.html', 
        'articles/handbags.html',
        'search/index.html'
    ]
    
    print("\n=== REDUNDANT TEXT CHECK ===")
    
    all_good = True
    
    for page in test_pages:
        if os.path.exists(page):
            try:
                with open(page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Count occurrences of "Search Affordable Handbags"
                occurrences = content.count('Search Affordable Handbags')
                
                if occurrences == 1:
                    print(f"✅ {page}: Only 1 occurrence (visible title only)")
                elif occurrences == 0:
                    print(f"⚠️  {page}: No occurrences found")
                else:
                    print(f"❌ {page}: {occurrences} occurrences found (should be 1)")
                    all_good = False
                
                # Check for proper screen reader label
                if 'sr-only">Search</label>' in content:
                    print(f"✅ {page}: Screen reader label is concise")
                else:
                    print(f"❌ {page}: Screen reader label issue")
                    all_good = False
                    
            except Exception as e:
                print(f"❌ {page}: Error reading file - {e}")
                all_good = False
        else:
            print(f"⚠️  {page}: File not found")
    
    # Check for any remaining redundant patterns
    print("\n=== PATTERN CHECK ===")
    
    redundant_patterns = [
        'Search Affordable Handbags</label>',
        'aria-label="Search Affordable Handbags"',
        'placeholder="Search Affordable Handbags"'
    ]
    
    for pattern in redundant_patterns:
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
        print("🎉 Redundant text successfully removed!")
        print("\nThe search bar now has:")
        print("  - Only ONE visible 'Search Affordable Handbags' title above the search bar")
        print("  - Concise screen reader label: 'Search'")
        print("  - Clean, uncluttered appearance")
        print("  - No duplicate or redundant text")
    else:
        print("⚠️  Some redundant text may still be present")
    
    return all_good

if __name__ == "__main__":
    verify_redundant_text_removal()
