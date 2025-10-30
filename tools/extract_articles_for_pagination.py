#!/usr/bin/env python3
"""
Extract and Sort Articles for Pagination

This script extracts all articles from the articles index page, sorts them by date (newest first),
and prepares them for pagination implementation.
"""

import re
from datetime import datetime

def extract_articles_from_html():
    """Extract articles from the HTML file and sort by date."""
    try:
        with open('articles/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    # Find all article cards
    article_pattern = r'<article class="article-card"[^>]*>(.*?)</article>'
    articles = re.findall(article_pattern, content, re.DOTALL)
    
    article_data = []
    
    for article in articles:
        # Extract title and link
        title_match = re.search(r'<h3><a href="([^"]+)"[^>]*>([^<]+)</a></h3>', article)
        if not title_match:
            continue
            
        link = title_match.group(1)
        title = title_match.group(2)
        
        # Extract date
        date_match = re.search(r'<span class="article-date">([^<]+)</span>', article)
        date_str = date_match.group(1) if date_match else "January 1, 2025"
        
        # Extract category
        category_match = re.search(r'<span class="article-category">([^<]+)</span>', article)
        category = category_match.group(1) if category_match else "Articles"
        
        # Extract reading time
        reading_time_match = re.search(r'<span class="article-reading-time">([^<]+)</span>', article)
        reading_time = reading_time_match.group(1) if reading_time_match else "5 min"
        
        # Extract description
        desc_match = re.search(r'<p>([^<]+)</p>', article)
        description = desc_match.group(1) if desc_match else ""
        
        # Extract image
        img_match = re.search(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', article)
        image_src = img_match.group(1) if img_match else ""
        image_alt = img_match.group(2) if img_match else ""
        
        # Extract data-category
        data_category_match = re.search(r'data-category="([^"]*)"', article)
        data_category = data_category_match.group(1) if data_category_match else ""
        
        # Parse date for sorting
        try:
            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
        except:
            parsed_date = datetime(2025, 1, 1)  # Default date
        
        article_data.append({
            'title': title,
            'link': link,
            'date': date_str,
            'parsed_date': parsed_date,
            'category': category,
            'data_category': data_category,
            'reading_time': reading_time,
            'description': description,
            'image_src': image_src,
            'image_alt': image_alt,
            'html': article
        })
    
    # Sort by date (newest first)
    article_data.sort(key=lambda x: x['parsed_date'], reverse=True)
    
    return article_data

def main():
    """Main function to extract and display articles."""
    print("=== EXTRACTING AND SORTING ARTICLES ===")
    
    articles = extract_articles_from_html()
    
    print(f"Found {len(articles)} articles")
    print("\nArticles sorted by date (newest first):")
    
    for i, article in enumerate(articles, 1):
        print(f"{i:2d}. {article['date']} - {article['title']}")
        print(f"     Category: {article['category']} | Data-category: {article['data_category']}")
        print(f"     Link: {article['link']}")
        print()
    
    # Calculate pagination
    articles_per_page = 10
    total_pages = (len(articles) + articles_per_page - 1) // articles_per_page
    
    print(f"=== PAGINATION CALCULATION ===")
    print(f"Total articles: {len(articles)}")
    print(f"Articles per page: {articles_per_page}")
    print(f"Total pages needed: {total_pages}")
    
    for page in range(1, total_pages + 1):
        start_idx = (page - 1) * articles_per_page
        end_idx = min(start_idx + articles_per_page, len(articles))
        page_articles = articles[start_idx:end_idx]
        print(f"Page {page}: Articles {start_idx + 1}-{end_idx} ({len(page_articles)} articles)")

if __name__ == "__main__":
    main()

