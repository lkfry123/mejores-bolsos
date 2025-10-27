#!/usr/bin/env python3
"""
GTM GA4 Enforcer - Ensures consistent Google Tag Manager implementation across HTML files.

This script:
1. Removes ALL existing GTM script loaders and direct gtag.js blocks
2. Inserts canonical GTM loader script in <head>
3. Inserts GTM noscript iframe immediately after <body>
4. Creates backups before modification
5. Reports summary of changes

Usage:
    python tools/gtm_ga4_enforcer.py [--dry-run] [--verbose]
    
Environment variables:
    GTM_CONTAINER_ID: GTM container ID (default: GTM-TCG7SMDD)
    GA4_MEASUREMENT_ID: GA4 measurement ID (default: G-H1Q1KL01RP)
    BACKUP_SUFFIX: Backup file suffix (default: .bak_gtmfix)
    TARGET_EXTENSIONS: Comma-separated file extensions (default: .html)
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple, Dict

# Configuration from environment variables
GTM_ID = os.environ.get("GTM_CONTAINER_ID", "GTM-TCG7SMDD")
GA4_ID = os.environ.get("GA4_MEASUREMENT_ID", "G-H1Q1KL01RP")
BACKUP_SUFFIX = os.environ.get("BACKUP_SUFFIX", ".bak_gtmfix")
EXTS = set(ext.strip().lower() for ext in os.environ.get("TARGET_EXTENSIONS", ".html").split(",")) if os.environ.get("TARGET_EXTENSIONS") else {".html"}

# Canonical GTM blocks
GTM_HEAD = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start': new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0], j=d.createElement(s), dl=l!='dataLayer'?'&l='+l:'';j.async=true; j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
"""

GTM_BODY = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""

# Regexes to remove any existing GTM loaders (handle small variations & minified)
RE_GTM_SCRIPT = re.compile(
    r"<!--\s*Google Tag Manager\s*-->.*?googletagmanager\.com/gtm\.js.*?<!--\s*End Google Tag Manager\s*-->",
    re.IGNORECASE | re.DOTALL
)
RE_GTM_NOSCRIPT = re.compile(
    r"<!--\s*Google Tag Manager \(noscript\)\s*-->.*?googletagmanager\.com/ns\.html\?id=.*?<!--\s*End Google Tag Manager \(noscript\)\s*-->",
    re.IGNORECASE | re.DOTALL
)

# Regexes to remove direct gtag.js implementations
RE_GTAG_SCRIPT = re.compile(
    r"<!--\s*Google tag \(gtag\.js\)\s*-->.*?googletagmanager\.com/gtag/js.*?<!--\s*End Google tag \(gtag\.js\)\s*-->",
    re.IGNORECASE | re.DOTALL
)
RE_GTAG_CONFIG = re.compile(
    r"gtag\('config',\s*['\"][^'\"]*['\"]\s*\)",
    re.IGNORECASE
)
RE_GTAG_INIT = re.compile(
    r"gtag\('js',\s*new Date\(\)\s*\)",
    re.IGNORECASE
)

# Additional patterns for various GTM implementations
RE_GTM_VARIANTS = [
    re.compile(r"googletagmanager\.com/gtm\.js\?id=", re.IGNORECASE),
    re.compile(r"googletagmanager\.com/ns\.html\?id=", re.IGNORECASE),
    re.compile(r"GTM-[A-Z0-9]+", re.IGNORECASE),
]

# Additional patterns for gtag variants
RE_GTAG_VARIANTS = [
    re.compile(r"googletagmanager\.com/gtag/js", re.IGNORECASE),
    re.compile(r"gtag\('config'", re.IGNORECASE),
    re.compile(r"gtag\('js'", re.IGNORECASE),
    re.compile(r"G-[A-Z0-9]+", re.IGNORECASE),
]

class GTMEnforcer:
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.stats = {
            'processed': 0,
            'modified': 0,
            'skipped': 0,
            'errors': 0,
            'backups_created': 0
        }
        self.errors: List[str] = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with optional verbosity control."""
        if level == "VERBOSE" and not self.verbose:
            return
        print(f"[{level}] {message}")
        
    def find_html_files(self, root_path: str) -> List[Path]:
        """Find all HTML files in the project tree."""
        root = Path(root_path)
        html_files = []
        
        for file_path in root.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in EXTS:
                html_files.append(file_path)
                
        return sorted(html_files)
    
    def create_backup(self, file_path: Path) -> bool:
        """Create backup of file before modification."""
        if self.dry_run:
            self.log(f"Would create backup: {file_path}{BACKUP_SUFFIX}", "VERBOSE")
            return True
            
        backup_path = file_path.with_suffix(file_path.suffix + BACKUP_SUFFIX)
        try:
            shutil.copy2(file_path, backup_path)
            self.stats['backups_created'] += 1
            self.log(f"Created backup: {backup_path}", "VERBOSE")
            return True
        except Exception as e:
            self.errors.append(f"Failed to create backup for {file_path}: {e}")
            return False
    
    def clean_gtm_content(self, content: str) -> str:
        """Remove all existing GTM and gtag implementations."""
        original_content = content
        
        # Remove GTM script blocks
        content = RE_GTM_SCRIPT.sub("", content)
        content = RE_GTM_NOSCRIPT.sub("", content)
        
        # Remove gtag script blocks
        content = RE_GTAG_SCRIPT.sub("", content)
        
        # Remove gtag config and init calls
        content = RE_GTAG_CONFIG.sub("", content)
        content = RE_GTAG_INIT.sub("", content)
        
        # Remove any remaining GTM/gtag references
        for pattern in RE_GTM_VARIANTS + RE_GTAG_VARIANTS:
            # Find and remove entire script tags containing these patterns
            script_pattern = re.compile(
                rf'<script[^>]*>.*?{pattern.pattern}.*?</script>',
                re.IGNORECASE | re.DOTALL
            )
            content = script_pattern.sub("", content)
            
            # Also remove noscript iframes
            noscript_pattern = re.compile(
                rf'<noscript[^>]*>.*?{pattern.pattern}.*?</noscript>',
                re.IGNORECASE | re.DOTALL
            )
            content = noscript_pattern.sub("", content)
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        return content
    
    def insert_gtm_head(self, content: str) -> str:
        """Insert GTM script in head section."""
        head_pattern = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
        match = head_pattern.search(content)
        
        if match:
            # Insert after opening head tag
            insert_pos = match.end()
            content = content[:insert_pos] + '\n' + GTM_HEAD + content[insert_pos:]
            self.log("Inserted GTM script in <head>", "VERBOSE")
        else:
            self.log("Warning: No <head> tag found, GTM script not inserted", "WARN")
            
        return content
    
    def insert_gtm_body(self, content: str) -> str:
        """Insert GTM noscript immediately after body tag."""
        body_pattern = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
        match = body_pattern.search(content)
        
        if match:
            # Insert after opening body tag
            insert_pos = match.end()
            content = content[:insert_pos] + '\n' + GTM_BODY + content[insert_pos:]
            self.log("Inserted GTM noscript in <body>", "VERBOSE")
        else:
            self.log("Warning: No <body> tag found, GTM noscript not inserted", "WARN")
            
        return content
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single HTML file."""
        self.stats['processed'] += 1
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()
            
            # Check if file is binary or too large
            if len(original_content) > 1024 * 1024:  # 1MB limit
                self.log(f"Skipping large file: {file_path}", "WARN")
                self.stats['skipped'] += 1
                return False
                
            # Clean existing GTM/gtag content
            cleaned_content = self.clean_gtm_content(original_content)
            
            # Insert GTM blocks
            final_content = self.insert_gtm_head(cleaned_content)
            final_content = self.insert_gtm_body(final_content)
            
            # Check if content changed
            if final_content == original_content:
                self.log(f"No changes needed: {file_path}", "VERBOSE")
                return False
            
            # Create backup
            if not self.create_backup(file_path):
                return False
            
            # Write modified content
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
            
            self.stats['modified'] += 1
            self.log(f"{'Would modify' if self.dry_run else 'Modified'}: {file_path}")
            return True
            
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            self.errors.append(error_msg)
            self.log(error_msg, "ERROR")
            self.stats['errors'] += 1
            return False
    
    def run(self, root_path: str = "."):
        """Main execution method."""
        self.log(f"GTM GA4 Enforcer starting...")
        self.log(f"GTM Container ID: {GTM_ID}")
        self.log(f"GA4 Measurement ID: {GA4_ID}")
        self.log(f"Target extensions: {', '.join(EXTS)}")
        self.log(f"Dry run: {self.dry_run}")
        
        # Find all HTML files
        html_files = self.find_html_files(root_path)
        self.log(f"Found {len(html_files)} HTML files to process")
        
        if not html_files:
            self.log("No HTML files found!", "WARN")
            return
        
        # Process each file
        for file_path in html_files:
            self.process_file(file_path)
        
        # Print summary
        self.print_summary()
        
        # Print errors if any
        if self.errors:
            self.log("\nErrors encountered:", "ERROR")
            for error in self.errors:
                self.log(f"  - {error}", "ERROR")
    
    def print_summary(self):
        """Print processing summary."""
        self.log("\n" + "="*50)
        self.log("PROCESSING SUMMARY")
        self.log("="*50)
        self.log(f"Files processed: {self.stats['processed']}")
        self.log(f"Files modified: {self.stats['modified']}")
        self.log(f"Files skipped: {self.stats['skipped']}")
        self.log(f"Errors: {self.stats['errors']}")
        self.log(f"Backups created: {self.stats['backups_created']}")
        
        if self.dry_run:
            self.log("\nThis was a DRY RUN - no files were actually modified")
        else:
            self.log(f"\nBackup suffix used: {BACKUP_SUFFIX}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Enforce GTM-only implementation across HTML files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  GTM_CONTAINER_ID    GTM container ID (default: GTM-TCG7SMDD)
  GA4_MEASUREMENT_ID  GA4 measurement ID (default: G-H1Q1KL01RP)
  BACKUP_SUFFIX       Backup file suffix (default: .bak_gtmfix)
  TARGET_EXTENSIONS   Comma-separated file extensions (default: .html)

Examples:
  python tools/gtm_ga4_enforcer.py
  python tools/gtm_ga4_enforcer.py --dry-run --verbose
  GTM_CONTAINER_ID=GTM-XXXXXXX python tools/gtm_ga4_enforcer.py
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making modifications'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed processing information'
    )
    
    parser.add_argument(
        '--root-path',
        default='.',
        help='Root path to search for HTML files (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Create and run enforcer
    enforcer = GTMEnforcer(dry_run=args.dry_run, verbose=args.verbose)
    enforcer.run(args.root_path)
    
    # Exit with error code if there were errors
    if enforcer.stats['errors'] > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
