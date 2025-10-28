#!/usr/bin/env python3
"""
Project Analysis and Cleanup Script

This script analyzes your project for:
1. Duplicate scripts and files
2. Backup file management
3. Potential conflicts
4. File structure issues

Usage:
    python3 tools/project_analyzer.py
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def analyze_backup_files():
    """Analyze all backup files in the project."""
    print("=== BACKUP FILE ANALYSIS ===")
    
    backup_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if '.bak_' in file:
                backup_files.append(Path(root) / file)
    
    # Group by backup type
    backup_types = defaultdict(list)
    for backup_file in backup_files:
        # Extract backup type from filename
        parts = backup_file.name.split('.bak_')
        if len(parts) > 1:
            backup_type = parts[1]
            backup_types[backup_type].append(backup_file)
    
    print(f"Total backup files: {len(backup_files)}")
    print(f"Backup types: {len(backup_types)}")
    print()
    
    for backup_type, files in backup_types.items():
        print(f"📁 {backup_type}: {len(files)} files")
        if len(files) <= 5:  # Show all if 5 or fewer
            for f in files:
                print(f"   {f}")
        else:  # Show first 3 and count
            for f in files[:3]:
                print(f"   {f}")
            print(f"   ... and {len(files) - 3} more")
        print()
    
    return backup_types

def analyze_active_files():
    """Analyze active (non-backup) files for conflicts."""
    print("=== ACTIVE FILE ANALYSIS ===")
    
    # Find all active HTML files
    html_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools'}]
        for file in files:
            if file.endswith('.html') and '.bak_' not in file and not file.startswith('.'):
                html_files.append(Path(root) / file)
    
    print(f"Active HTML files: {len(html_files)}")
    
    # Check for tracking implementations
    gtm_count = 0
    gtag_count = 0
    ga4_refs = 0
    issues = []
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Count implementations
            gtm_scripts = len(re.findall(r'googletagmanager\.com/gtm\.js', content, re.IGNORECASE))
            gtag_scripts = len(re.findall(r'googletagmanager\.com/gtag/js', content, re.IGNORECASE))
            gtag_calls = len(re.findall(r'gtag\(', content, re.IGNORECASE))
            ga4_references = len(re.findall(r'G-H1Q1KL01RP', content))
            
            gtm_count += gtm_scripts
            gtag_count += gtag_scripts + gtag_calls
            ga4_refs += ga4_references
            
            # Check for issues
            if gtm_scripts > 1:
                issues.append(f"{html_file}: {gtm_scripts} GTM scripts (should be 1)")
            if gtag_scripts > 0 or gtag_calls > 0:
                issues.append(f"{html_file}: {gtag_scripts + gtag_calls} gtag implementations (should be 0)")
            if ga4_references > 0:
                issues.append(f"{html_file}: {ga4_references} GA4 references (should be 0)")
                
        except Exception as e:
            issues.append(f"{html_file}: Error reading file - {e}")
    
    print(f"GTM scripts found: {gtm_count}")
    print(f"gtag implementations found: {gtag_count}")
    print(f"GA4 references found: {ga4_refs}")
    print()
    
    if issues:
        print("⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("✅ All active files are clean!")
    
    return len(issues) == 0

def analyze_js_files():
    """Analyze JavaScript files for conflicts."""
    print("\n=== JAVASCRIPT FILE ANALYSIS ===")
    
    js_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', 'out', 'tools'}]
        for file in files:
            if file.endswith('.js') and '.bak_' not in file and not file.startswith('.'):
                js_files.append(Path(root) / file)
    
    print(f"Active JavaScript files: {len(js_files)}")
    
    for js_file in js_files:
        print(f"📄 {js_file}")
        try:
            with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for tracking code
            gtag_refs = len(re.findall(r'gtag', content, re.IGNORECASE))
            gtm_refs = len(re.findall(r'GTM-TCG7SMDD', content))
            ga4_refs = len(re.findall(r'G-H1Q1KL01RP', content))
            
            if gtag_refs > 0 or gtm_refs > 0 or ga4_refs > 0:
                print(f"   ⚠️  Contains tracking code: gtag={gtag_refs}, GTM={gtm_refs}, GA4={ga4_refs}")
            else:
                print(f"   ✅ Clean")
                
        except Exception as e:
            print(f"   ❌ Error reading: {e}")
    
    return js_files

def cleanup_old_backups():
    """Clean up old backup files, keeping only the most recent."""
    print("\n=== BACKUP CLEANUP ===")
    
    # Keep only the most recent backup type
    backup_types = ['bak_complete_fix', 'bak_gtm_precise', 'bak_gtm_cleanup', 'bak_gtm_dedupe_fix', 'bak_gtm_dedupe', 'bak_gtmfix']
    
    # Find all backup files
    all_backups = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if '.bak_' in file:
                all_backups.append(Path(root) / file)
    
    # Group by original file
    original_files = defaultdict(list)
    for backup in all_backups:
        # Extract original filename
        original_name = backup.name.split('.bak_')[0] + '.html'
        original_path = backup.parent / original_name
        original_files[str(original_path)].append(backup)
    
    # Keep only the most recent backup for each file
    kept_count = 0
    removed_count = 0
    
    for original_file, backups in original_files.items():
        # Sort by backup type priority (most recent first)
        backups_sorted = []
        for backup_type in backup_types:
            for backup in backups:
                if backup_type in backup.name:
                    backups_sorted.append(backup)
                    break
        
        # Keep the first (most recent) backup, remove others
        if backups_sorted:
            kept_backup = backups_sorted[0]
            kept_count += 1
            print(f"✅ Keeping: {kept_backup}")
            
            # Remove older backups
            for old_backup in backups_sorted[1:]:
                try:
                    old_backup.unlink()
                    removed_count += 1
                    print(f"🗑️  Removed: {old_backup}")
                except Exception as e:
                    print(f"❌ Error removing {old_backup}: {e}")
    
    print(f"\nBackup cleanup complete:")
    print(f"   Kept: {kept_count} files")
    print(f"   Removed: {removed_count} files")
    
    return kept_count, removed_count

def main():
    """Main analysis function."""
    print("🔍 PROJECT ANALYSIS AND CLEANUP")
    print("=" * 50)
    
    # Analyze backup files
    backup_types = analyze_backup_files()
    
    # Analyze active files
    active_files_clean = analyze_active_files()
    
    # Analyze JavaScript files
    js_files = analyze_js_files()
    
    # Cleanup old backups
    kept, removed = cleanup_old_backups()
    
    # Summary
    print("\n=== SUMMARY ===")
    print(f"✅ Active files clean: {active_files_clean}")
    print(f"📁 JavaScript files: {len(js_files)}")
    print(f"🗂️  Backup files cleaned: {removed} removed, {kept} kept")
    
    if active_files_clean:
        print("\n🎉 Your project is clean and ready for deployment!")
        print("All tracking conflicts have been resolved.")
    else:
        print("\n⚠️  Some issues remain in active files.")
        print("Run the complete GTM fix script to resolve them.")

if __name__ == "__main__":
    main()
