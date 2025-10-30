#!/usr/bin/env python3
"""
Check Article Links

This script checks for broken article links across all HTML files.
"""

import os
import re
from pathlib import Path

def check_article_links():
    """Check for broken article links in all HTML files."""
    print("=== CHECKING ARTICLE LINKS ===")
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools', 'scripts'}]
        for file in files:
            if file.endswith('.html') and not file.startswith('.') and '.bak_' not in file:
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files to check")
    print()
    
    broken_links = []
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            continue
        
        # Find article links with directory-style URLs
        article_links = re.findall(r'href="(/articles/[^"]+/)"', content)
        
        for link in article_links:
            # Convert directory-style URL to file-style URL
            expected_file = link.rstrip('/') + '.html'
            file_exists = os.path.exists(expected_file.lstrip('/'))
            
            if not file_exists:
                broken_links.append({
                    'file': str(file_path),
                    'link': link,
                    'expected': expected_file
                })
    
    if broken_links:
        print("❌ BROKEN ARTICLE LINKS FOUND:")
        print()
        for item in broken_links:
            print(f"File: {item['file']}")
            print(f"  Broken link: {item['link']}")
            print(f"  Should be: {item['expected']}")
            print()
    else:
        print("✅ No broken article links found!")
    
    # Check for other common link patterns
    print("\n=== CHECKING OTHER LINK PATTERNS ===")
    
    other_broken = []
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            continue
        
        # Check for other directory-style links
        patterns = [
            (r'href="(/quiz/[^"]+/)"', 'quiz'),
            (r'href="(/about/[^"]+/)"', 'about'),
            (r'href="(/contact/[^"]+/)"', 'contact'),
            (r'href="(/terms/[^"]+/)"', 'terms')
        ]
        
        for pattern, category in patterns:
            links = re.findall(pattern, content)
            for link in links:
                expected_file = link.rstrip('/') + '/index.html'
                file_exists = os.path.exists(expected_file.lstrip('/'))
                
                if not file_exists:
                    other_broken.append({
                        'file': str(file_path),
                        'link': link,
                        'category': category
                    })
    
    if other_broken:
        print("❌ OTHER BROKEN LINKS FOUND:")
        print()
        for item in other_broken:
            print(f"File: {item['file']}")
            print(f"  {item['category']} link: {item['link']}")
            print()
    else:
        print("✅ No other broken links found!")
    
    print(f"\n=== SUMMARY ===")
    print(f"Total broken article links: {len(broken_links)}")
    print(f"Total other broken links: {len(other_broken)}")
    
    if broken_links or other_broken:
        print("\n💡 TIP: Directory-style URLs (ending with /) need to be changed to file-style URLs (.html)")
    else:
        print("\n🎉 All links are working correctly!")

if __name__ == "__main__":
    check_article_links()
