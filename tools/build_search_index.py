#!/usr/bin/env python3
"""
Build Search Index

This script scans HTML files and builds a search index JSON file.
"""

import os
import re
from pathlib import Path
from datetime import datetime

def extract_article_data(file_path):
    """Extract article data from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Untitled"
    
    # Extract description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
    description = desc_match.group(1).strip() if desc_match else ""
    
    # Extract date from article-meta or use file modification time
    date_match = re.search(r'<span class="article-meta">(.*?)</span>', content, re.IGNORECASE)
    if date_match:
        date_str = date_match.group(1).strip()
        # Try to parse common date formats
        try:
            if "October" in date_str and "2025" in date_str:
                parsed_date = datetime.strptime(date_str, "%B %d, %Y")
                date = parsed_date.strftime("%Y-%m-%d")
            else:
                date = "2025-01-01"  # Default fallback
        except:
            date = "2025-01-01"
    else:
        # Use file modification time
        try:
            mtime = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        except:
            date = "2025-01-01"
    
    # Determine category based on path
    category = "General"
    if "/articles/handbags" in str(file_path):
        category = "Handbags"
    elif "/articles/backpacks" in str(file_path):
        category = "Backpacks"
    elif "/articles/wallets" in str(file_path):
        category = "Wallets"
    elif "/articles/tote-bags" in str(file_path):
        category = "Tote Bags"
    elif "/categories/" in str(file_path):
        if "handbags" in str(file_path):
            category = "Handbags"
        elif "backpacks" in str(file_path):
            category = "Backpacks"
        elif "wallets" in str(file_path):
            category = "Wallets"
        elif "tote-bags" in str(file_path):
            category = "Tote Bags"
    
    # Generate tags based on content
    tags = []
    content_lower = content.lower()
    
    # Brand tags
    brands = ["coach", "osprey", "tory burch", "valentino", "gucci", "prada", "louis vuitton", "bottega veneta"]
    for brand in brands:
        if brand in content_lower:
            tags.append(brand)
    
    # Style tags
    styles = ["crossbody", "tote", "backpack", "wallet", "clutch", "hobo", "satchel", "messenger", "laptop", "work", "travel", "hiking", "professional", "casual", "elegant", "minimalist"]
    for style in styles:
        if style in content_lower:
            tags.append(style)
    
    # Price tags
    if "affordable" in content_lower or "budget" in content_lower:
        tags.append("affordable")
    if "under 100" in content_lower or "under $100" in content_lower:
        tags.append("under 100")
    if "luxury" in content_lower or "expensive" in content_lower:
        tags.append("luxury")
    
    # Remove duplicates and limit tags
    tags = list(set(tags))[:10]
    
    # Generate URL
    url = str(file_path).replace("\\", "/")
    if url.startswith("./"):
        url = url[2:]
    if not url.startswith("/"):
        url = "/" + url
    
    return {
        "title": title,
        "url": url,
        "category": category,
        "tags": tags,
        "date": date,
        "excerpt": description
    }

def find_article_files():
    """Find all article and category HTML files."""
    files = []
    
    # Articles directory
    articles_dir = Path("articles")
    if articles_dir.exists():
        for file_path in articles_dir.rglob("*.html"):
            if not file_path.name.startswith('.') and '.bak_' not in str(file_path):
                files.append(file_path)
    
    # Categories directory
    categories_dir = Path("categories")
    if categories_dir.exists():
        for file_path in categories_dir.rglob("*.html"):
            if not file_path.name.startswith('.') and '.bak_' not in str(file_path):
                files.append(file_path)
    
    # Main pages
    main_pages = ["index.html", "privacy-policy.html", "affiliate-disclosure.html"]
    for page in main_pages:
        if os.path.exists(page):
            files.append(Path(page))
    
    return files

def main():
    """Main execution."""
    print("=== BUILDING SEARCH INDEX ===")
    print("Scanning HTML files and building search index...")
    print()
    
    files = find_article_files()
    print(f"Found {len(files)} files to process:")
    print()
    
    articles = []
    
    for file_path in files:
        print(f"Processing {file_path}...")
        article_data = extract_article_data(file_path)
        if article_data:
            articles.append(article_data)
            print(f"  ✅ {article_data['title']}")
        else:
            print(f"  ❌ Failed to extract data")
    
    # Sort by date (newest first)
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Write JSON file
    import json
    try:
        with open('search-index.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Search index written to search-index.json")
        print(f"📊 Total articles indexed: {len(articles)}")
        
        # Show some sample entries
        print("\nSample entries:")
        for i, article in enumerate(articles[:3]):
            print(f"  {i+1}. {article['title']} ({article['category']})")
        
    except Exception as e:
        print(f"❌ Error writing search-index.json: {e}")

if __name__ == "__main__":
    main()
