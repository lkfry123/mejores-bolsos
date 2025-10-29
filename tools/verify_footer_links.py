#!/usr/bin/env python3
"""
Footer Link Verification

This script verifies that footer links are correctly fixed across key pages.
"""

import os
import re
from pathlib import Path

def verify_footer_links(file_path):
    """Verify footer links in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False
    
    issues = []
    
    # Check for old trailing slash patterns
    if re.search(r'href="/articles/handbags/"', content):
        issues.append("handbags link has trailing slash")
    if re.search(r'href="/articles/backpacks/"', content):
        issues.append("backpacks link has trailing slash")
    if re.search(r'href="/articles/wallets/"', content):
        issues.append("wallets link has trailing slash")
    if re.search(r'href="/articles/tote-bags/"', content):
        issues.append("tote-bags link has trailing slash")
    if re.search(r'href="/privacy-policy/"', content):
        issues.append("privacy-policy link has trailing slash")
    if re.search(r'href="/affiliate-disclosure/"', content):
        issues.append("affiliate-disclosure link has trailing slash")
    
    # Check for correct .html patterns
    correct_patterns = [
        r'href="/articles/handbags\.html"',
        r'href="/articles/backpacks\.html"',
        r'href="/articles/wallets\.html"',
        r'href="/articles/tote-bags\.html"'
    ]
    
    for pattern in correct_patterns:
        if not re.search(pattern, content):
            issues.append(f"Missing correct pattern: {pattern}")
    
    if issues:
        print(f"❌ {file_path}: {', '.join(issues)}")
        return False
    else:
        print(f"✅ {file_path}: All footer links correct")
        return True

def main():
    """Main execution."""
    print("=== FOOTER LINK VERIFICATION ===")
    print("Checking key pages for footer link correctness...")
    print()
    
    # Key pages to check
    key_pages = [
        "index.html",
        "privacy-policy.html", 
        "affiliate-disclosure.html",
        "articles/handbags.html",
        "articles/wallets.html",
        "articles/backpacks.html",
        "articles/tote-bags.html"
    ]
    
    all_good = True
    
    for page in key_pages:
        if os.path.exists(page):
            if not verify_footer_links(page):
                all_good = False
        else:
            print(f"⚠️  {page}: File not found")
            all_good = False
    
    print()
    if all_good:
        print("🎉 All key pages have correct footer links!")
    else:
        print("⚠️  Some pages still have footer link issues")

if __name__ == "__main__":
    main()
