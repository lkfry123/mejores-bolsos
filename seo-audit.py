#!/usr/bin/env python3

import re
import os
from datetime import datetime

# A) INVENTORY PAGES
def get_html_files():
    """Collect all HTML files and convert to final URLs"""
    html_files = []
    
    # Root level files
    root_files = [
        'index.html',
        'privacy-policy.html', 
        'affiliate-disclosure.html'
    ]
    
    # Articles
    articles = [
        '3-functional-diaper-bags-moms-2025.html',
        '3-functional-university-tote-bags-2025.html',
        '3-popular-amazon-tote-bags-2025.html',
        '3-reusable-shopping-tote-bags-2025.html',
        '3-rfid-security-wallets-2025.html',
        '3-stylish-professional-backpacks-2025.html',
        '3-wristlet-wallets-women-2025.html',
        'affordable-elegant-casual-handbags-wedding-guest-2025.html',
        'backpacks.html',
        'best-durable-stylish-backpacks-2025.html',
        'best-lightweight-travel-backpacks-2025.html',
        'best-wedding-handbags-2025.html',
        'fun-unique-gift-wallets-2025.html',
        'handbags.html',
        'how-to-choose-perfect-handbag-2025.html',
        'index.html',
        'laptop-backpacks-protection-style-2025.html',
        'minimalist-daily-bag-2025.html',
        'top-5-professional-women-wallets-2025.html',
        'tote-bags.html',
        'travel-light-adventure-bags-2025.html',
        'wallets.html'
    ]
    
    # Categories
    categories = [
        'backpacks/index.html',
        'handbags/index.html', 
        'tote-bags/index.html',
        'wallets/index.html',
        'index.html'
    ]
    
    # Spanish files
    es_files = [
        'index.html',
        'politica-privacidad.html',
        'aviso-afiliados.html'
    ]
    
    es_articles = [
        '3-bolsos-panales-funcionales-mamas-2025.html',
        '3-carteras-rfid-seguridad-2025.html',
        '3-carteras-wristlet-mujeres-2025.html',
        '3-mochilas-profesionales-estilosas-2025.html',
        '3-tote-bags-funcionales-universidad-2025.html',
        '3-tote-bags-populares-amazon-2025.html',
        '3-tote-bags-reutilizables-compras-2025.html',
        'best-durable-stylish-backpacks-2025.html',
        'bolso-minimalista-dia-dia-2025.html',
        'bolsos-casual-elegantes-asequibles-invitadas-bodas-2025.html',
        'bolsos-de-mano.html',
        'carteras-divertidas-unicas-regalo-2025.html',
        'carteras.html',
        'como-elegir-bolso-mano-perfecto-2025.html',
        'index.html',
        'las-mejores-mochilas-mano-viajar-ligero-2025.html',
        'mejores-bolsos-mano-bodas-2025.html',
        'mochilas-para-laptop-proteccion-estilo-2025.html',
        'mochilas.html',
        'resistentes-estilo-mejores-mochilas-dia-dia-2025.html',
        'top-5-carteras-mujeres-profesionales-2025.html',
        'tote-bags.html',
        'viajar-ligera-bolsos-aventureras-2025.html'
    ]
    
    es_categories = [
        'bolsos-de-mano/index.html',
        'carteras/index.html',
        'mochilas/index.html',
        'tote-bags/index.html',
        'index.html'
    ]
    
    # Quiz
    quiz_files = [
        'quiz/bag-personality/index.html'
    ]
    
    # Build inventory
    for file in root_files:
        html_files.append(('', file))
    
    for file in articles:
        html_files.append(('articles/', file))
    
    for file in categories:
        html_files.append(('categories/', file))
    
    for file in es_files:
        html_files.append(('es/', file))
    
    for file in es_articles:
        html_files.append(('es/articulos/', file))
    
    for file in es_categories:
        html_files.append(('es/categorias/', file))
    
    for file in quiz_files:
        html_files.append(('', file))
    
    return html_files

def convert_to_final_url(path, file):
    """Convert file path to final URL"""
    # Handle index.html files
    if file == 'index.html':
        if path:
            return f"https://affordable-handbags.com/{path.rstrip('/')}/"
        else:
            return "https://affordable-handbags.com/"
    # Handle other .html files
    else:
        name = file.replace('.html', '')
        return f"https://affordable-handbags.com/{path}{name}/"

def classify_url(url):
    """Classify URL as EN or ES"""
    if '/es/' in url:
        return 'ES'
    else:
        return 'EN'

# B) PARSE SITEMAP
def parse_sitemap():
    """Parse sitemap.xml and extract URLs"""
    sitemap_urls = []
    
    with open('sitemap.xml', 'r') as f:
        content = f.read()
    
    # Extract all <loc> URLs
    pattern = r'<loc>(https://affordable-handbags\.com[^<]+)</loc>'
    matches = re.findall(pattern, content)
    
    for url in matches:
        sitemap_urls.append(url)
    
    return sitemap_urls

# C) COMPARE
def compare_inventory_sitemap(inventory_urls, sitemap_urls):
    """Compare inventory vs sitemap"""
    inventory_set = set(inventory_urls)
    sitemap_set = set(sitemap_urls)
    
    missing_from_sitemap = inventory_set - sitemap_set
    stale_in_sitemap = sitemap_set - inventory_set
    
    return missing_from_sitemap, stale_in_sitemap

def main():
    print("=== SEO AUDIT FOR BILINGUAL STATIC SITE ===\n")
    
    # A) INVENTORY PAGES
    print("A) INVENTORY PAGES")
    print("-" * 50)
    
    html_files = get_html_files()
    inventory_urls = []
    english_urls = []
    spanish_urls = []
    
    for path, file in html_files:
        final_url = convert_to_final_url(path, file)
        inventory_urls.append(final_url)
        
        if classify_url(final_url) == 'EN':
            english_urls.append(final_url)
        else:
            spanish_urls.append(final_url)
    
    print(f"Total HTML files: {len(html_files)}")
    print(f"English URLs: {len(english_urls)}")
    print(f"Spanish URLs: {len(spanish_urls)}")
    print()
    
    # B) PARSE SITEMAP
    print("B) PARSE SITEMAP")
    print("-" * 50)
    
    sitemap_urls = parse_sitemap()
    sitemap_english = [url for url in sitemap_urls if '/es/' not in url]
    sitemap_spanish = [url for url in sitemap_urls if '/es/' in url]
    
    print(f"Sitemap total URLs: {len(sitemap_urls)}")
    print(f"Sitemap English URLs: {len(sitemap_english)}")
    print(f"Sitemap Spanish URLs: {len(sitemap_spanish)}")
    print()
    
    # C) COMPARE
    print("C) COMPARE INVENTORY vs SITEMAP")
    print("-" * 50)
    
    missing_from_sitemap, stale_in_sitemap = compare_inventory_sitemap(inventory_urls, sitemap_urls)
    
    print(f"Missing from sitemap: {len(missing_from_sitemap)}")
    if missing_from_sitemap:
        print("Sample missing URLs:")
        for url in sorted(list(missing_from_sitemap))[:5]:
            print(f"  - {url}")
    print()
    
    print(f"Stale in sitemap: {len(stale_in_sitemap)}")
    if stale_in_sitemap:
        print("Sample stale URLs:")
        for url in sorted(list(stale_in_sitemap))[:5]:
            print(f"  - {url}")
    print()
    
    # D) CANONICAL + HREFLANG CHECK
    print("D) CANONICAL + HREFLANG CHECK")
    print("-" * 50)
    
    # Sample a few English pages for canonical/hreflang check
    sample_english = [
        'articles/wallets.html',
        'articles/handbags.html', 
        'index.html'
    ]
    
    for file in sample_english:
        print(f"Checking: {file}")
        # This would require parsing HTML files - simplified for now
        print(f"  - Would check canonical and hreflang tags")
    print()
    
    # E) SUMMARY
    print("E) SUMMARY")
    print("-" * 50)
    print(f"Total inventory URLs: {len(inventory_urls)}")
    print(f"Total sitemap URLs: {len(sitemap_urls)}")
    print(f"Missing from sitemap: {len(missing_from_sitemap)}")
    print(f"Stale in sitemap: {len(stale_in_sitemap)}")
    print()
    
    # Show some examples
    print("Sample English URLs from inventory:")
    for url in sorted(english_urls)[:5]:
        print(f"  - {url}")
    print()
    
    print("Sample Spanish URLs from inventory:")
    for url in sorted(spanish_urls)[:5]:
        print(f"  - {url}")

if __name__ == "__main__":
    main()
