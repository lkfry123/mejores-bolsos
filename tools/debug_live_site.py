#!/usr/bin/env python3
"""
GTM Live Site Debugger - Helps identify gtag.js sources on live site

This script helps you identify where gtag.js implementations might be coming from
on your live site that aren't in your local files.

Usage:
    python3 tools/debug_live_site.py
"""

import requests
import re
from urllib.parse import urljoin, urlparse

def check_page_for_gtag(url: str) -> dict:
    """Check a live page for gtag implementations."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
        
        # Look for gtag implementations
        gtag_js_matches = re.findall(r'https://www\.googletagmanager\.com/gtag/js[^"\'>\s]*', content, re.IGNORECASE)
        gtag_dest_matches = re.findall(r'https://www\.googletagmanager\.com/gtag/destination[^"\'>\s]*', content, re.IGNORECASE)
        gtag_calls = re.findall(r'gtag\([^)]*\)', content, re.IGNORECASE)
        ga4_refs = re.findall(r'G-H1Q1KL01RP', content)
        
        return {
            "url": url,
            "status": "success",
            "gtag_js_urls": gtag_js_matches,
            "gtag_dest_urls": gtag_dest_matches,
            "gtag_calls": gtag_calls,
            "ga4_references": ga4_refs,
            "has_gtag": len(gtag_js_matches) > 0 or len(gtag_dest_matches) > 0 or len(gtag_calls) > 0
        }
    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "error": str(e),
            "has_gtag": False
        }

def main():
    """Main debugging function."""
    print("=== GTM Live Site Debugger ===")
    print("Checking live site for gtag.js implementations...")
    print()
    
    # URLs to check
    urls_to_check = [
        "https://affordable-handbags.com/",
        "https://affordable-handbags.com/articles/",
        "https://affordable-handbags.com/articles/backpacks/",
        "https://affordable-handbags.com/es/",
        "https://affordable-handbags.com/es/articulos/"
    ]
    
    found_issues = []
    
    for url in urls_to_check:
        print(f"Checking: {url}")
        result = check_page_for_gtag(url)
        
        if result["status"] == "error":
            print(f"  ❌ Error: {result['error']}")
        elif result["has_gtag"]:
            print(f"  ⚠️  FOUND GTAG IMPLEMENTATIONS:")
            if result["gtag_js_urls"]:
                print(f"    gtag.js URLs: {result['gtag_js_urls']}")
            if result["gtag_dest_urls"]:
                print(f"    gtag destination URLs: {result['gtag_dest_urls']}")
            if result["gtag_calls"]:
                print(f"    gtag() calls: {len(result['gtag_calls'])} found")
            if result["ga4_references"]:
                print(f"    GA4 ID references: {len(result['ga4_references'])} found")
            found_issues.append(result)
        else:
            print(f"  ✅ Clean - no gtag implementations found")
        print()
    
    if found_issues:
        print("=== ISSUES FOUND ===")
        print("Your live site still has gtag.js implementations!")
        print()
        print("Possible sources:")
        print("1. Files not deployed properly")
        print("2. Server-side includes/templates")
        print("3. CDN serving cached versions")
        print("4. Third-party widgets/plugins")
        print("5. Server configuration injecting scripts")
        print()
        print("Solutions:")
        print("1. Re-deploy ALL HTML files")
        print("2. Clear CDN cache completely")
        print("3. Check server configuration")
        print("4. Look for server-side template files")
        print("5. Check for any CMS or dynamic content")
    else:
        print("🎉 No gtag implementations found on live site!")
        print("The Safari errors might be due to browser caching.")

if __name__ == "__main__":
    main()
