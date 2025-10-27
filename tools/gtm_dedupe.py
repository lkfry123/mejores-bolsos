#!/usr/bin/env python3
"""
GTM Deduplication Script - Ensures exactly one GTM loader per HTML file

This script:
1. Finds all GTM loader blocks for the same container ID
2. Keeps only the first one in <head>, removes duplicates
3. Ensures noscript iframe exists after <body>
4. Creates backups before modification
5. Reports summary of changes

Usage:
    python3 tools/gtm_dedupe.py
    
Environment variables:
    GTM_CONTAINER_ID: GTM container ID (default: GTM-TCG7SMDD)
    BACKUP_SUFFIX: Backup file suffix (default: .bak_gtm_dedupe)
    TARGET_EXTENSIONS: Comma-separated file extensions (default: .html)
"""

import os
import re
import shutil
from pathlib import Path

GTM_ID = os.environ.get("GTM_CONTAINER_ID", "GTM-TCG7SMDD")
BACKUP_SUFFIX = os.environ.get("BACKUP_SUFFIX", ".bak_gtm_dedupe")
EXTS = set(x.strip().lower() for x in os.environ.get("TARGET_EXTENSIONS", ".html").split(",")) if os.environ.get("TARGET_EXTENSIONS") else {".html"}

RE_HEAD_OPEN = re.compile(r"<head[^>]*>", re.IGNORECASE)
RE_BODY_OPEN = re.compile(r"<body[^>]*>", re.IGNORECASE)

# Flexible match for GTM loader block (comment-wrapped), same container
RE_GTM_BLOCK = re.compile(
    r"<!--\s*Google Tag Manager\s*-->.*?googletagmanager\.com/gtm\.js\?id=(?:'\+i\+dl|'+i\+dl|[^\"'>]*)(.*?)<!--\s*End Google Tag Manager\s*-->",
    re.IGNORECASE | re.DOTALL
)

def normalize_gtm_head(gtm_id: str) -> str:
    return f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start': new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0], j=d.createElement(s), dl=l!='dataLayer'?'&l='+l:'';j.async=true; j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{gtm_id}');</script>
<!-- End Google Tag Manager -->
"""

def normalize_gtm_body(gtm_id: str) -> str:
    return f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_id}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""

def all_gtm_blocks(text: str, gtm_id: str):
    # collect spans for blocks that clearly reference GTM_ID
    spans = []
    for m in RE_GTM_BLOCK.finditer(text):
        block = m.group(0)
        if gtm_id in block:
            spans.append((m.start(), m.end(), block))
    return spans

def ensure_one_in_head(text: str, gtm_id: str):
    blocks = all_gtm_blocks(text, gtm_id)
    if not blocks:
        return text, 0, False  # no GTM, no changes

    # Remove all GTM blocks first
    for s, e, _ in reversed(blocks):
        text = text[:s] + text[e:]

    # Insert a single canonical block immediately after <head>
    head_match = RE_HEAD_OPEN.search(text)
    if head_match:
        insert_at = head_match.end()
        text = text[:insert_at] + "\n" + normalize_gtm_head(gtm_id) + "\n" + text[insert_at:]
    else:
        # If no <head>, append at top (rare)
        text = normalize_gtm_head(gtm_id) + "\n" + text

    return text, len(blocks)-1, True  # duplicates removed count, changed

def ensure_noscript_after_body(text: str, gtm_id: str):
    # already present?
    body_noscript = normalize_gtm_body(gtm_id).splitlines()[0]  # first line comment
    if body_noscript.lower() in text.lower():
        return text, False

    m = RE_BODY_OPEN.search(text)
    if not m:
        return text, False
    insert_at = m.end()
    text = text[:insert_at] + "\n" + normalize_gtm_body(gtm_id) + "\n" + text[insert_at:]
    return text, True

def process_html(path: Path):
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        return (str(path), "unreadable", 0, False)

    original = raw

    raw, dup_removed, changed_head = ensure_one_in_head(raw, GTM_ID)
    raw, added_noscript = ensure_noscript_after_body(raw, GTM_ID)

    changed = (raw != original)
    if changed:
        backup = path.with_suffix(path.suffix + BACKUP_SUFFIX)
        try:
            shutil.copy2(path, backup)
        except Exception:
            pass
        path.write_text(raw, encoding="utf-8")
    return (str(path), "updated" if changed else "no_change", dup_removed, added_noscript)

def main():
    changed = 0
    total_dups_removed = 0
    noscript_added = 0
    scanned = 0
    skipped = 0

    for dp, _, files in os.walk("."):
        if any(x in dp for x in ("/.git", "/node_modules", "/dist", "/build", "/.next", "/out")):
            continue
        for fn in files:
            ext = Path(fn).suffix.lower()
            if ext not in EXTS:
                continue
            scanned += 1
            p = Path(dp) / fn
            path, status, dups, added = process_html(p)
            if status == "updated":
                changed += 1
            else:
                if status != "no_change":
                    skipped += 1
            total_dups_removed += max(dups, 0)
            noscript_added += 1 if added else 0

    print("=== GTM Deduper Summary ===")
    print(f"GTM Container: {GTM_ID}")
    print(f"Scanned HTML files: {scanned}")
    print(f"Files changed: {changed}")
    print(f"Duplicate GTM blocks removed: {total_dups_removed}")
    print(f"noscript inserted: {noscript_added}")
    print("Backups suffix:", BACKUP_SUFFIX)

if __name__ == "__main__":
    main()
