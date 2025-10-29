#!/usr/bin/env python3
"""
Simple Link Checker for Homepage

This script checks if all the links on the homepage point to existing files.
"""

import os
import re
from pathlib import Path

def check_homepage_links():
    """Check all links in the homepage."""
    print("=== HOMEPAGE LINK CHECKER ===")
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ index.html not found")
        return False
    
    # Find all href links
    href_pattern = r'href="([^"]+)"'
    links = re.findall(href_pattern, content)
    
    print(f"Found {len(links)} links to check:")
    print()
    
    broken_links = []
    working_links = []
    
    for link in links:
        if link.startswith('http'):
            # External link - skip for now
            working_links.append(link)
            print(f"🌐 {link} (external)")
            continue
            
        if link.startswith('#'):
            # Anchor link - skip
            working_links.append(link)
            print(f"🔗 {link} (anchor)")
            continue
            
        if link.startswith('/'):
            # Absolute path
            file_path = link[1:]  # Remove leading slash
        else:
            # Relative path
            file_path = link
            
        # Handle query parameters
        if '?' in file_path:
            file_path = file_path.split('?')[0]
            
        # Special case for root path
        if file_path == '':
            file_path = 'index.html'
            
        # Check if file exists
        if os.path.exists(file_path):
            working_links.append(link)
            print(f"✅ {link}")
        elif os.path.exists(file_path + '.html'):
            working_links.append(link)
            print(f"✅ {link} (redirects to {file_path}.html)")
        elif os.path.exists(file_path + '/index.html'):
            working_links.append(link)
            print(f"✅ {link} (serves {file_path}/index.html)")
        else:
            broken_links.append(link)
            print(f"❌ {link} (FILE NOT FOUND)")
    
    print()
    print("=== SUMMARY ===")
    print(f"✅ Working links: {len(working_links)}")
    print(f"❌ Broken links: {len(broken_links)}")
    
    if broken_links:
        print("\nBroken links:")
        for link in broken_links:
            print(f"  - {link}")
        return False
    else:
        print("\n🎉 All links are working!")
        return True

if __name__ == "__main__":
    check_homepage_links()
