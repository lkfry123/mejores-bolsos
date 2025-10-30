#!/usr/bin/env python3
"""
Debug Specific Filter Button Issues

This script helps identify what might be appearing when pressing specific filter buttons.
"""

import re

def debug_specific_filters():
    """Debug what appears when pressing specific filter buttons."""
    print("=== DEBUGGING SPECIFIC FILTER BUTTONS ===")
    
    try:
        with open('articles/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading articles index file: {e}")
        return
    
    # Check for any error messages or no-results messages
    print(f"\n=== CHECKING FOR ERROR MESSAGES ===")
    
    # Look for no-results messages
    no_results_patterns = [
        r'No hay artículos disponibles',
        r'No articles available',
        r'no-category-results',
        r'no-results-message'
    ]
    
    for pattern in no_results_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"  ⚠️  Found: {pattern} - {len(matches)} occurrences")
        else:
            print(f"  ✅ Not found: {pattern}")
    
    # Check JavaScript for potential issues
    print(f"\n=== CHECKING JAVASCRIPT FOR ISSUES ===")
    try:
        with open('assets/script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
    except Exception as e:
        print(f"❌ Error reading JS file: {e}")
        return
    
    # Check for showNoCategoryResults function
    if 'showNoCategoryResults' in js_content:
        print("  ✅ showNoCategoryResults function exists")
        
        # Extract the function to see what it does
        no_results_match = re.search(r'function showNoCategoryResults\([^)]*\)\s*\{[^}]*\}', js_content, re.DOTALL)
        if no_results_match:
            print("  📝 Function content:")
            print("    " + no_results_match.group(0).replace('\n', '\n    '))
    else:
        print("  ❌ showNoCategoryResults function missing")
    
    # Check for console.log statements that might show what's happening
    console_logs = re.findall(r'console\.log\([^)]*\)', js_content)
    if console_logs:
        print(f"\n=== CONSOLE LOG MESSAGES ===")
        for log in console_logs:
            print(f"  📝 {log}")
    
    # Check specific categories
    print(f"\n=== CHECKING SPECIFIC CATEGORIES ===")
    categories_to_check = ['mochilas', 'carteras', 'tote-bags']
    
    for category in categories_to_check:
        # Count articles in this category
        article_count = len(re.findall(f'data-category="{category}"', content))
        print(f"  {category}: {article_count} articles")
        
        if article_count == 0:
            print(f"    ⚠️  WARNING: No articles found for {category}")
        elif article_count < 3:
            print(f"    ⚠️  WARNING: Very few articles for {category}")
    
    print(f"\n=== POTENTIAL ISSUES ===")
    print("1. No-results message appearing when it shouldn't")
    print("2. Console error messages")
    print("3. JavaScript execution errors")
    print("4. CSS styling issues")
    print("5. DOM manipulation problems")
    
    print(f"\n=== DEBUGGING STEPS ===")
    print("1. Open browser developer tools (F12)")
    print("2. Go to Console tab")
    print("3. Click on 'Backpacks' button")
    print("4. Look for any error messages or unexpected output")
    print("5. Check if 'showNoCategoryResults' is being called")
    print("6. Repeat for 'Wallets' and 'Tote Bags'")

if __name__ == "__main__":
    debug_specific_filters()
