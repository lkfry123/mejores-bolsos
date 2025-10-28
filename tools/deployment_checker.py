#!/usr/bin/env python3
"""
Live Site vs Local Files Comparison Tool

This tool helps identify discrepancies between your local clean files
and what's actually running on your live site.

Usage:
    python3 tools/deployment_checker.py
"""

import os
import re
from pathlib import Path

def check_local_files():
    """Check local files for tracking implementations."""
    print("=== LOCAL FILES CHECK ===")
    
    html_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools'}]
        for file in files:
            if file.endswith('.html') and '.bak_' not in file and not file.startswith('.'):
                html_files.append(Path(root) / file)
    
    gtag_count = 0
    ga4_count = 0
    gtm_count = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            gtag_refs = len(re.findall(r'gtag\(', content, re.IGNORECASE))
            ga4_refs = len(re.findall(r'G-H1Q1KL01RP', content))
            gtm_refs = len(re.findall(r'googletagmanager\.com/gtm\.js', content, re.IGNORECASE))
            
            gtag_count += gtag_refs
            ga4_count += ga4_refs
            gtm_count += gtm_refs
            
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
    
    print(f"Local HTML files: {len(html_files)}")
    print(f"gtag() calls: {gtag_count}")
    print(f"GA4 references: {ga4_count}")
    print(f"GTM scripts: {gtm_count}")
    
    if gtag_count == 0 and ga4_count == 0 and gtm_count == len(html_files):
        print("✅ Local files are PERFECT - clean GTM-only implementation")
        return True
    else:
        print("⚠️  Local files have issues")
        return False

def check_assets_folder():
    """Check assets folder for tracking code."""
    print("\n=== ASSETS FOLDER CHECK ===")
    
    js_files = []
    for root, dirs, files in os.walk("assets"):
        for file in files:
            if file.endswith('.js') and not file.startswith('.'):
                js_files.append(Path(root) / file)
    
    print(f"JavaScript files in assets: {len(js_files)}")
    
    tracking_found = False
    for js_file in js_files:
        try:
            with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            gtag_refs = len(re.findall(r'gtag', content, re.IGNORECASE))
            gtm_refs = len(re.findall(r'GTM-TCG7SMDD', content))
            ga4_refs = len(re.findall(r'G-H1Q1KL01RP', content))
            
            if gtag_refs > 0 or gtm_refs > 0 or ga4_refs > 0:
                print(f"⚠️  {js_file}: Contains tracking code (gtag={gtag_refs}, GTM={gtm_refs}, GA4={ga4_refs})")
                tracking_found = True
            else:
                print(f"✅ {js_file}: Clean")
                
        except Exception as e:
            print(f"❌ Error reading {js_file}: {e}")
    
    if not tracking_found:
        print("✅ Assets folder is clean - no tracking code found")
    
    return not tracking_found

def generate_deployment_instructions():
    """Generate step-by-step deployment instructions."""
    print("\n=== DEPLOYMENT INSTRUCTIONS ===")
    print("Your local files are clean, but your live site still has gtag.js implementations.")
    print("This means your live site has OLD files that haven't been updated.")
    print()
    print("🔧 STEP-BY-STEP SOLUTION:")
    print()
    print("1. 📁 BACKUP YOUR LIVE SITE")
    print("   - Download all files from your live server")
    print("   - Keep a backup before making changes")
    print()
    print("2. 📤 UPLOAD CLEAN FILES")
    print("   - Upload ALL 75 HTML files from your local project")
    print("   - Overwrite existing files completely")
    print("   - Make sure to upload the entire project structure")
    print()
    print("3. 🗂️  VERIFY FILE STRUCTURE")
    print("   - Ensure all folders are uploaded (articles/, es/, categories/, etc.)")
    print("   - Check that assets/ folder is uploaded")
    print("   - Verify all subdirectories are present")
    print()
    print("4. 🧹 CLEAR ALL CACHES")
    print("   - Clear CDN cache (Cloudflare, etc.)")
    print("   - Clear server cache")
    print("   - Clear browser cache")
    print()
    print("5. 🧪 TEST DEPLOYMENT")
    print("   - Open Safari in private/incognito mode")
    print("   - Visit https://affordable-handbags.com/articles/")
    print("   - Check Safari Developer Tools → Console")
    print("   - Look for the gtag.js error URLs")
    print()
    print("6. ✅ VERIFICATION CHECKLIST")
    print("   - No 404 errors for gtag.js")
    print("   - No 404 errors for destination")
    print("   - Only GTM script loading")
    print("   - Clean Safari console")
    print()
    print("🎯 EXPECTED RESULT:")
    print("After proper deployment, Safari should show NO gtag.js errors!")

def main():
    """Main execution."""
    print("🔍 DEPLOYMENT CHECKER - Live Site vs Local Files")
    print("=" * 60)
    
    # Check local files
    local_clean = check_local_files()
    
    # Check assets folder
    assets_clean = check_assets_folder()
    
    # Generate instructions
    if local_clean and assets_clean:
        generate_deployment_instructions()
    else:
        print("\n⚠️  Local files need cleaning first!")
        print("Run the complete GTM fix script before deploying.")

if __name__ == "__main__":
    main()
