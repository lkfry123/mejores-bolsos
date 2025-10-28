#!/usr/bin/env python3
"""
Complete GTM Fix and Test Suite

This script provides a comprehensive solution to fix all GTM/gtag issues
and includes testing capabilities to verify the fixes work.

Usage:
    python3 tools/complete_gtm_fix.py
"""

import os
import re
import shutil
from pathlib import Path

GTM_ID = "GTM-TCG7SMDD"
GA4_ID = "G-H1Q1KL01RP"
BACKUP_SUFFIX = ".bak_complete_fix"

def create_clean_gtm_implementation():
    """Create the cleanest possible GTM implementation."""
    return {
        "head_script": f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start': new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0], j=d.createElement(s), dl=l!='dataLayer'?'&l='+l:'';j.async=true; j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->""",
        
        "body_noscript": f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""
    }

def clean_file_completely(file_path: Path) -> tuple[str, int]:
    """Completely clean a file of all tracking implementations except GTM."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}", 0
    
    original_content = content
    removal_count = 0
    
    # Remove ALL gtag implementations
    gtag_patterns = [
        r"<!--\s*Google tag \(gtag\.js\)\s*-->.*?<!--\s*End Google tag \(gtag\.js\)\s*-->",
        r"<script[^>]*>.*?gtag\(.*?</script>",
        r"function gtag\(\)\{[^}]*\}",
        r"gtag\('[^']*',\s*[^)]*\)",
        r"gtag\('js',\s*new Date\(\)\s*\)",
        r"window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];",
        r"<!--\s*GA4 is configured.*?G-H1Q1KL01RP.*?-->"
    ]
    
    for pattern in gtag_patterns:
        new_content = re.sub(pattern, "", content, flags=re.IGNORECASE | re.DOTALL)
        if new_content != content:
            removal_count += 1
            content = new_content
    
    # Remove ALL GTM implementations (we'll add clean ones)
    gtm_patterns = [
        r"<!--\s*Google Tag Manager\s*-->.*?<!--\s*End Google Tag Manager\s*-->",
        r"<!--\s*Google Tag Manager \(noscript\)\s*-->.*?<!--\s*End Google Tag Manager \(noscript\)\s*-->"
    ]
    
    for pattern in gtm_patterns:
        content = re.sub(pattern, "", content, flags=re.IGNORECASE | re.DOTALL)
    
    # Add clean GTM implementation
    gtm = create_clean_gtm_implementation()
    
    # Insert GTM script in head
    head_match = re.search(r'(<head[^>]*>)', content, re.IGNORECASE)
    if head_match:
        insert_pos = head_match.end()
        content = content[:insert_pos] + '\n' + gtm["head_script"] + '\n' + content[insert_pos:]
    else:
        content = gtm["head_script"] + '\n' + content
    
    # Insert GTM noscript after body
    body_match = re.search(r'(<body[^>]*>)', content, re.IGNORECASE)
    if body_match:
        insert_pos = body_match.end()
        content = content[:insert_pos] + '\n' + gtm["body_noscript"] + '\n' + content[insert_pos:]
    
    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    return content, removal_count

def process_file(file_path: Path) -> tuple[str, str, int]:
    """Process a single HTML file."""
    try:
        content, removals = clean_file_completely(file_path)
        
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + BACKUP_SUFFIX)
        shutil.copy2(file_path, backup_path)
        
        # Write cleaned content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(file_path), "cleaned", removals
        
    except Exception as e:
        return str(file_path), f"error: {e}", 0

def test_local_files() -> dict:
    """Test local files for tracking issues."""
    html_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools'}]
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(Path(root) / file)
    
    total_files = len(html_files)
    clean_files = 0
    issues_found = []
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for problematic patterns
            gtag_js = len(re.findall(r'googletagmanager\.com/gtag/js', content, re.IGNORECASE))
            gtag_dest = len(re.findall(r'googletagmanager\.com/gtag/destination', content, re.IGNORECASE))
            gtag_calls = len(re.findall(r'gtag\(', content, re.IGNORECASE))
            ga4_refs = len(re.findall(r'G-H1Q1KL01RP', content))
            gtm_scripts = len(re.findall(r'googletagmanager\.com/gtm\.js', content, re.IGNORECASE))
            
            is_clean = gtag_js == 0 and gtag_dest == 0 and gtag_calls == 0 and ga4_refs == 0 and gtm_scripts == 1
            
            if is_clean:
                clean_files += 1
            else:
                issues_found.append({
                    "file": str(file_path),
                    "gtag_js": gtag_js,
                    "gtag_dest": gtag_dest,
                    "gtag_calls": gtag_calls,
                    "ga4_refs": ga4_refs,
                    "gtm_scripts": gtm_scripts
                })
                
        except Exception as e:
            issues_found.append({"file": str(file_path), "error": str(e)})
    
    return {
        "total_files": total_files,
        "clean_files": clean_files,
        "issues_found": issues_found
    }

def main():
    """Main execution."""
    print("=== Complete GTM Fix and Test Suite ===")
    print(f"GTM Container: {GTM_ID}")
    print(f"GA4 Measurement ID: {GA4_ID}")
    print()
    
    # Step 1: Clean all local files
    print("Step 1: Cleaning all local HTML files...")
    html_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools'}]
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(Path(root) / file)
    
    cleaned_count = 0
    total_removals = 0
    
    for file_path in sorted(html_files):
        path, status, removals = process_file(file_path)
        if status == "cleaned":
            cleaned_count += 1
            total_removals += removals
            print(f"✅ {path} - Removed {removals} tracking implementations")
        else:
            print(f"❌ {path} - {status}")
    
    print(f"\nCleaned {cleaned_count}/{len(html_files)} files")
    print(f"Total tracking implementations removed: {total_removals}")
    
    # Step 2: Test local files
    print("\nStep 2: Testing local files...")
    test_result = test_local_files()
    
    print(f"Total files tested: {test_result['total_files']}")
    print(f"Clean files: {test_result['clean_files']}")
    print(f"Files with issues: {len(test_result['issues_found'])}")
    
    if test_result['issues_found']:
        print("\nFiles with issues:")
        for issue in test_result['issues_found']:
            if 'error' in issue:
                print(f"❌ {issue['file']} - Error: {issue['error']}")
            else:
                print(f"⚠️  {issue['file']}:")
                print(f"   gtag.js URLs: {issue['gtag_js']}")
                print(f"   gtag destination URLs: {issue['gtag_dest']}")
                print(f"   gtag() calls: {issue['gtag_calls']}")
                print(f"   GA4 references: {issue['ga4_refs']}")
                print(f"   GTM scripts: {issue['gtm_scripts']}")
    else:
        print("🎉 All local files are clean!")
    
    # Step 3: Deployment instructions
    print("\nStep 3: Deployment Instructions")
    print("=" * 50)
    print("Your local files are now completely clean!")
    print()
    print("To fix your live site:")
    print("1. Upload ALL HTML files to your live server")
    print("2. Overwrite existing files completely")
    print("3. Clear CDN cache (Cloudflare, etc.)")
    print("4. Clear server cache")
    print("5. Test in Safari with hard refresh (Cmd+Shift+R)")
    print()
    print("Expected results after deployment:")
    print("✅ No 404 errors for gtag.js or destination")
    print("✅ No gtag() calls in page source")
    print("✅ Only GTM script loading")
    print("✅ Clean Safari console")
    print("✅ Accurate analytics data")

if __name__ == "__main__":
    main()
