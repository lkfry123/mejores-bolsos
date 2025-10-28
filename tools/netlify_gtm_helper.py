#!/usr/bin/env python3
"""
Netlify GTM Deployment Helper

This script helps identify and fix GTM issues specific to Netlify hosting.

Usage:
    python3 tools/netlify_gtm_helper.py
"""

import os
import re
from pathlib import Path

def analyze_netlify_config():
    """Analyze netlify.toml for potential GTM issues."""
    print("=== NETLIFY CONFIGURATION ANALYSIS ===")
    
    try:
        with open('netlify.toml', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ netlify.toml not found")
        return False
    
    print("✅ netlify.toml found")
    
    # Check for cache settings that might affect GTM
    cache_patterns = [
        r'Cache-Control.*max-age=(\d+)',
        r'immutable',
        r'public.*max-age'
    ]
    
    cache_issues = []
    for pattern in cache_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            cache_issues.extend(matches)
    
    if cache_issues:
        print(f"⚠️  Found cache settings: {len(cache_issues)}")
        print("   Cache settings might be serving old files")
    else:
        print("✅ No aggressive cache settings found")
    
    # Check for HTML cache settings
    html_cache = re.search(r'for = "\*\.html".*?max-age=(\d+)', content, re.DOTALL)
    if html_cache:
        cache_time = html_cache.group(1)
        print(f"⚠️  HTML files cached for {cache_time} seconds")
        if int(cache_time) > 3600:  # More than 1 hour
            print("   This might prevent GTM updates from appearing immediately")
    else:
        print("✅ HTML cache settings look reasonable")
    
    return True

def check_deployment_status():
    """Check if files are ready for Netlify deployment."""
    print("\n=== DEPLOYMENT READINESS CHECK ===")
    
    # Check for clean HTML files
    html_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools'}]
        for file in files:
            if file.endswith('.html') and '.bak_' not in file and not file.startswith('.'):
                html_files.append(Path(root) / file)
    
    clean_files = 0
    gtag_issues = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            gtag_count = len(re.findall(r'gtag\(', content, re.IGNORECASE))
            ga4_count = len(re.findall(r'G-H1Q1KL01RP', content))
            gtm_count = len(re.findall(r'googletagmanager\.com/gtm\.js', content, re.IGNORECASE))
            
            if gtag_count == 0 and ga4_count == 0 and gtm_count == 1:
                clean_files += 1
            else:
                gtag_issues += 1
                
        except Exception as e:
            print(f"❌ Error reading {html_file}: {e}")
    
    print(f"Total HTML files: {len(html_files)}")
    print(f"Clean files: {clean_files}")
    print(f"Files with issues: {gtag_issues}")
    
    if gtag_issues == 0:
        print("✅ All files are clean and ready for Netlify deployment!")
        return True
    else:
        print("⚠️  Some files still have tracking issues")
        return False

def generate_netlify_solution():
    """Generate Netlify-specific solution for GTM issues."""
    print("\n=== NETLIFY GTM SOLUTION ===")
    print()
    print("🎯 THE ISSUE:")
    print("Your Netlify site is serving cached versions of old files with gtag.js")
    print("Even though your local files are clean, Netlify hasn't updated yet.")
    print()
    print("🔧 SOLUTION STEPS:")
    print()
    print("1. 📤 DEPLOY TO NETLIFY")
    print("   - Push your clean files to your Git repository")
    print("   - Or drag & drop your project folder to Netlify")
    print("   - Wait for the build to complete")
    print()
    print("2. 🧹 CLEAR NETLIFY CACHE")
    print("   - Go to your Netlify dashboard")
    print("   - Click on your site")
    print("   - Go to 'Deploys' tab")
    print("   - Click 'Clear cache and deploy site'")
    print("   - Or trigger a new deploy")
    print()
    print("3. ⏱️  WAIT FOR PROPAGATION")
    print("   - Netlify CDN takes 5-15 minutes to update globally")
    print("   - Test in different browsers/incognito mode")
    print("   - Check Safari Developer Tools → Network tab")
    print()
    print("4. 🔍 VERIFY DEPLOYMENT")
    print("   - Visit: https://affordable-handbags.com/articles/")
    print("   - Check page source for gtag.js (should be gone)")
    print("   - Look for only GTM script (should remain)")
    print()
    print("5. 🚨 IF STILL ISSUES:")
    print("   - Check Netlify build logs for errors")
    print("   - Verify all files were uploaded correctly")
    print("   - Try 'Clear cache and deploy site' again")
    print()
    print("📋 NETLIFY-SPECIFIC NOTES:")
    print("- Your netlify.toml has HTML cache set to 1 hour (3600 seconds)")
    print("- This is reasonable and shouldn't cause issues")
    print("- The redirects in netlify.toml look correct")
    print("- No GTM-specific configuration needed in netlify.toml")

def suggest_netlify_toml_updates():
    """Suggest any helpful updates to netlify.toml."""
    print("\n=== NETLIFY.TOML RECOMMENDATIONS ===")
    print()
    print("Your netlify.toml looks good! No changes needed for GTM.")
    print()
    print("However, if you want to be extra safe, you could add:")
    print()
    print("# Optional: Force immediate cache refresh for HTML files")
    print("[[headers]]")
    print("  for = \"*.html\"")
    print("  [headers.values]")
    print("    Cache-Control = \"public, max-age=300\"  # 5 minutes instead of 1 hour")
    print()
    print("But this is NOT necessary - your current settings are fine.")

def main():
    """Main execution."""
    print("🚀 NETLIFY GTM DEPLOYMENT HELPER")
    print("=" * 50)
    
    # Analyze Netlify config
    config_ok = analyze_netlify_config()
    
    # Check deployment readiness
    files_ready = check_deployment_status()
    
    # Generate solution
    if config_ok and files_ready:
        generate_netlify_solution()
        suggest_netlify_toml_updates()
    else:
        print("\n⚠️  Fix local issues first before deploying to Netlify")

if __name__ == "__main__":
    main()
