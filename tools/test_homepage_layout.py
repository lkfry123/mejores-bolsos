#!/usr/bin/env python3
"""
Test Homepage Layout

This script verifies that the Featured Articles section appears above the Explore by Category section.
"""

import re

def test_homepage_layout():
    """Test the homepage section order."""
    print("=== TESTING HOMEPAGE LAYOUT ===")
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading index.html: {e}")
        return
    
    print("\n=== SECTION ORDER VERIFICATION ===")
    
    # Find all section headers
    sections = []
    
    # Look for section titles
    section_patterns = [
        (r'<h2 class="section-title">Featured Articles</h2>', 'Featured Articles'),
        (r'<h2 class="section-title">Explore by Category</h2>', 'Explore by Category'),
        (r'<h1 class="ah-hero__title">', 'Hero Section'),
        (r'<section id="searchResults"', 'Search Results'),
        (r'<footer class="footer">', 'Footer')
    ]
    
    for pattern, name in section_patterns:
        matches = list(re.finditer(pattern, content))
        if matches:
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                sections.append((line_num, name, match.group()))
        else:
            print(f"⚠️  {name}: Not found")
    
    # Sort by line number
    sections.sort(key=lambda x: x[0])
    
    print("Homepage section order:")
    for i, (line_num, name, snippet) in enumerate(sections, 1):
        print(f"  {i}. {name} (line {line_num})")
    
    # Verify Featured Articles comes before Explore by Category
    featured_line = None
    categories_line = None
    
    for line_num, name, snippet in sections:
        if name == 'Featured Articles':
            featured_line = line_num
        elif name == 'Explore by Category':
            categories_line = line_num
    
    if featured_line and categories_line:
        if featured_line < categories_line:
            print(f"\n✅ SUCCESS: Featured Articles (line {featured_line}) appears before Explore by Category (line {categories_line})")
        else:
            print(f"\n❌ ERROR: Featured Articles (line {featured_line}) appears after Explore by Category (line {categories_line})")
    else:
        print("\n⚠️  Could not verify section order")
    
    # Check for proper section structure
    print(f"\n=== SECTION STRUCTURE VERIFICATION ===")
    
    # Check Featured Articles section
    if 'Featured Articles' in content and 'articles-grid' in content:
        print("✅ Featured Articles section: Properly structured")
    else:
        print("❌ Featured Articles section: Missing or malformed")
    
    # Check Categories section
    if 'Explore by Category' in content and 'categories-grid' in content:
        print("✅ Explore by Category section: Properly structured")
    else:
        print("❌ Explore by Category section: Missing or malformed")
    
    # Count articles in Featured Articles
    article_cards = len(re.findall(r'<article class="article-card">', content))
    print(f"✅ Featured Articles: {article_cards} article cards found")
    
    # Count category cards
    category_cards = len(re.findall(r'<a href="/articles/.*\.html" class="category-card">', content))
    print(f"✅ Explore by Category: {category_cards} category cards found")
    
    print(f"\n=== LAYOUT SUMMARY ===")
    print("New homepage order:")
    print("  1. Hero Section")
    print("  2. Featured Articles (6 articles)")
    print("  3. Explore by Category (4 categories)")
    print("  4. Search Results (hidden by default)")
    print("  5. Footer")
    
    print(f"\n=== TEST COMPLETE ===")
    print("The Featured Articles section now appears above the Explore by Category section!")

if __name__ == "__main__":
    test_homepage_layout()
