#!/usr/bin/env python3
"""
Test Filter Button Functionality

This script creates a simple test to verify filter buttons work correctly.
"""

def create_filter_test():
    """Create a simple test page to verify filtering works."""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Filter Test</title>
    <style>
        .article-card {
            border: 1px solid #ccc;
            margin: 10px;
            padding: 10px;
            display: block;
        }
        .filter-btn {
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
            border: 1px solid #ccc;
            background: white;
        }
        .filter-btn.active {
            background-color: #0e7a6d;
            color: white;
        }
        .articles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
    </style>
</head>
<body>
    <h1>Filter Test Page</h1>
    
    <div class="filters">
        <button class="filter-btn active" data-category="todos">All</button>
        <button class="filter-btn" data-category="mochilas">Backpacks</button>
        <button class="filter-btn" data-category="carteras">Wallets</button>
        <button class="filter-btn" data-category="tote-bags">Tote Bags</button>
    </div>
    
    <div class="articles-grid">
        <article class="article-card" data-category="mochilas">
            <h3>Backpack Article 1</h3>
            <span class="article-date">October 17, 2025</span>
        </article>
        <article class="article-card" data-category="mochilas">
            <h3>Backpack Article 2</h3>
            <span class="article-date">January 12, 2025</span>
        </article>
        <article class="article-card" data-category="carteras">
            <h3>Wallet Article 1</h3>
            <span class="article-date">January 30, 2025</span>
        </article>
        <article class="article-card" data-category="carteras">
            <h3>Wallet Article 2</h3>
            <span class="article-date">January 15, 2025</span>
        </article>
        <article class="article-card" data-category="tote-bags">
            <h3>Tote Bag Article 1</h3>
            <span class="article-date">January 30, 2025</span>
        </article>
        <article class="article-card" data-category="tote-bags">
            <h3>Tote Bag Article 2</h3>
            <span class="article-date">January 30, 2025</span>
        </article>
    </div>
    
    <script>
        function filterArticlesByCategory(category, articleCards) {
            console.log('Filtering by category:', category);
            let hasResults = false;
            const filteredCards = [];
            
            // Función para mostrar animación de fade in
            function showCard(card) {
                card.style.display = 'block';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
                card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            }

            // Función para ocultar tarjeta
            function hideCard(card) {
                card.style.display = 'none';
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
            }
            
            // Función para extraer fecha del artículo
            function getArticleDate(card) {
                const dateElement = card.querySelector('.article-date');
                if (dateElement) {
                    const dateText = dateElement.textContent.trim();
                    return new Date(dateText);
                }
                return new Date(0);
            }
            
            // Primero, filtrar artículos por categoría
            articleCards.forEach(card => {
                const cardCategory = card.getAttribute('data-category');
                console.log('Article category:', cardCategory, 'Filter category:', category);
                
                if (category === 'todos' || cardCategory === category) {
                    filteredCards.push(card);
                    hasResults = true;
                } else {
                    hideCard(card);
                }
            });
            
            console.log('Filtered cards:', filteredCards.length);
            
            // Si hay resultados, ordenar por fecha (más reciente primero)
            if (hasResults && filteredCards.length > 0) {
                filteredCards.sort((a, b) => {
                    const dateA = getArticleDate(a);
                    const dateB = getArticleDate(b);
                    return dateB - dateA;
                });
                
                // Reorganizar el DOM con los artículos ordenados
                const articlesGrid = document.querySelector('.articles-grid');
                if (articlesGrid) {
                    const fragment = document.createDocumentFragment();
                    filteredCards.forEach(card => {
                        fragment.appendChild(card);
                    });
                    articlesGrid.innerHTML = '';
                    articlesGrid.appendChild(fragment);
                }
                
                // Mostrar los artículos ordenados
                filteredCards.forEach(card => {
                    showCard(card);
                });
            }
            
            return filteredCards;
        }
        
        // Initialize filtering
        document.addEventListener('DOMContentLoaded', function() {
            const filterButtons = document.querySelectorAll('.filter-btn');
            const articleCards = document.querySelectorAll('.article-card');
            
            filterButtons.forEach(button => {
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    const category = this.getAttribute('data-category');
                    console.log('Button clicked:', category);
                    
                    // Remove active class from all buttons
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    
                    // Add active class to clicked button
                    this.classList.add('active');
                    
                    // Filter articles
                    filterArticlesByCategory(category, articleCards);
                });
            });
        });
    </script>
</body>
</html>'''
    
    with open('filter-test.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Filter test page created: filter-test.html")
    print("   Open this file in your browser to test filtering")
    print("   Check browser console for debug messages")

if __name__ == "__main__":
    create_filter_test()
