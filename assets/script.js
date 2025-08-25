// ===== FUNCIONALIDADES PRINCIPALES =====

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todas las funcionalidades
    initMobileMenu();
    initSearchFunctionality();
    initCategoryFiltering();
    initSmoothScroll();
    initExternalLinks();
    initScrollEffects();
});

// ===== MENÚ MÓVIL =====
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Cerrar menú al hacer clic en un enlace
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
        
        // Cerrar menú al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
}

// ===== FUNCIONALIDAD DE BÚSQUEDA =====
function initSearchFunctionality() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.querySelector('.search-btn');
    const clearSearchBtn = document.getElementById('clearSearch');
    const searchSuggestions = document.getElementById('searchSuggestions');
    
    if (searchInput && searchBtn) {
        // Búsqueda al escribir (con debounce)
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const searchTerm = this.value.toLowerCase().trim();
                if (searchTerm.length >= 1) {
                    showSearchSuggestions(searchTerm);
                } else {
                    hideSearchSuggestions();
                }
                if (searchTerm.length >= 2) {
                    performSearch(searchTerm);
                } else if (searchTerm.length === 0) {
                    clearSearch();
                }
            }, 200);
        });
        
        // Búsqueda al hacer clic en el botón
        searchBtn.addEventListener('click', function() {
            const searchTerm = searchInput.value.toLowerCase().trim();
            if (searchTerm.length >= 2) {
                performSearch(searchTerm);
                hideSearchSuggestions();
            }
        });
        
        // Búsqueda al presionar Enter
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const searchTerm = this.value.toLowerCase().trim();
                if (searchTerm.length >= 2) {
                    performSearch(searchTerm);
                    hideSearchSuggestions();
                }
            }
        });
        
        // Ocultar sugerencias al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
                hideSearchSuggestions();
            }
        });
        
        // Limpiar búsqueda
        if (clearSearchBtn) {
            clearSearchBtn.addEventListener('click', clearSearch);
        }
    }
}

// Base de datos de artículos para búsqueda
const articlesDatabase = [
    {
        title: "Resistentes y con Estilo: Las Mejores Mochilas para Tu Día a Día 2025",
        description: "Descubre por qué invertir en una mochila de alta calidad es esencial. Guía completa con las mejores mochilas resistentes y estilosas para el uso diario.",
        category: "Mochilas",
        url: "/articulos/resistentes-estilo-mejores-mochilas-dia-dia-2025.html",
        image: "../photos/LOVEVOOK%20Laptop%20Backpack%20for%20Women%2015.6in%20Computer%20Backpacks%20Dark%20Green.jpg",
        date: "30 Enero 2025",
        tags: ["mochilas", "calidad", "resistente", "día a día", "durabilidad", "protección", "comodidad", "organización", "versatilidad", "LOVEVOOK", "SwissGear", "The North Face", "TSA", "FlexVent", "2025"]
    },
    {
        title: "Los 10 Mejores Bolsos de Mano 2025",
        description: "Descubre los bolsos más elegantes y funcionales del año. Desde opciones de lujo hasta alternativas asequibles.",
        category: "Bolsos de Mano",
        url: "/articulos/mejores-bolsos-de-mano-2025.html",
        image: "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=250&fit=crop",
        date: "15 Enero 2025",
        tags: ["bolsos", "mano", "elegantes", "lujo", "funcionales", "2025"]
    },
    {
        title: "Cómo Elegir el Bolso de Mano Perfecto para Cada Ocasión 2025",
        description: "Guía completa para elegir el bolso ideal según la ocasión: bodas, cenas, oficina y viajes. Recomendaciones expertas con enlaces de compra.",
        category: "Bolsos de Mano",
        url: "/articulos/como-elegir-bolso-mano-perfecto-2025.html",
        image: "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=250&fit=crop",
        date: "20 Enero 2025",
        tags: ["bolsos", "mano", "guía", "ocasiones", "bodas", "cenas", "oficina", "viajes", "2025"]
    },
    {
        title: "Mochilas para Laptop: Protección y Estilo 2025",
        description: "Descubre las mejores mochilas para laptop con protección antirrobo, puertos USB y diseño TSA. Guía completa con reseñas detalladas.",
        category: "Mochilas",
        url: "/articulos/mochilas-para-laptop-proteccion-estilo-2025.html",
        image: "../photos/VOLHER%20Laptop%20Backpack,Business%20Travel%20Anti%20Theft%20Slim%20Durable%20Laptops%20Backpack%20with%20USB%20Charging%20Port,Water%20Resistant.jpg",
        date: "25 Enero 2025",
        tags: ["mochilas", "laptop", "antirrobo", "USB", "TSA", "protección", "2025"]
    },
    {
        title: "3 Tote Bags Populares en Amazon 2025",
        description: "Descubre las 3 tote bags más populares en Amazon 2025. Guía completa con reseñas detalladas, comparativas y enlaces de compra.",
        category: "Tote Bags",
        url: "/articulos/3-tote-bags-populares-amazon-2025.html",
        image: "../photos/BAGSMART%20Tote%20Bag%20for%20Women,%20Foldable%20Tote%20Bag%20With%20Zipper%20Travel%20Large%20Shoulder%20Bag%20Handbag%20for%20Work.jpg",
        date: "30 Enero 2025",
        tags: ["tote bags", "amazon", "populares", "compras", "sostenible", "2025"]
    },
    {
        title: "Los 3 Mejores Bolsos de Mano para Bodas 2025: Elegancia y Estilo",
        description: "Descubre los 3 mejores bolsos de mano para bodas 2025. Guía completa con reseñas detalladas, comparativas y enlaces de compra para encontrar el bolso perfecto para tu día especial.",
        category: "Bolsos de Mano",
        url: "/articulos/mejores-bolsos-mano-bodas-2025.html",
        image: "../photos/CHARMING%20TAILOR%20Classic%20Satin%20Clutch%20Bag%20Handbag.jpg",
        date: "30 Enero 2025",
        tags: ["bolsos de mano", "bodas", "clutch", "elegante", "satin", "2025", "novia", "eventos"]
    },
    {
        title: "3 Mochilas Profesionales Estilosas 2025: Elegancia y Funcionalidad",
        description: "Descubre las 3 mochilas profesionales más estilosas para mujeres 2025. Guía completa con reseñas detalladas, comparativas y enlaces de compra para encontrar la mochila perfecta para tu trabajo y estilo.",
        category: "Mochilas",
        url: "/articulos/3-mochilas-profesionales-estilosas-2025.html",
        image: "../photos/LOVEVOOK%20Anti%20Theft%20Slim%20Backpack%20for%20Women,%20Fit%2015.6%20Inch%20Laptop%20Beige-Khaqi.jpg",
        date: "30 Enero 2025",
        tags: ["mochilas", "profesionales", "estilosas", "laptop", "trabajo", "2025", "elegante", "funcional"]
    },
    {
        title: "3 Bolsos de Pañales Funcionales para Mamás 2025: Organización y Estilo",
        description: "Descubre los 3 mejores bolsos de pañales funcionales para mamás 2025. Guía completa con reseñas detalladas, comparativas y enlaces de compra para mantener todo organizado con tu bebé.",
        category: "Tote Bags",
        url: "/articulos/3-bolsos-panales-funcionales-mamas-2025.html",
        image: "../photos/Diaper%20Bag%20Tote%20Large%20Tote%20Baby%20Bag%20Boy%20Diaper%20Bag%20Stylish%20Girl%20Diaper%20Ba%20Shoulder%20Mommy%20Bag.jpg",
        date: "30 Enero 2025",
        tags: ["bolsos de pañales", "mamás", "bebés", "organización", "funcional", "2025", "tote bags", "diaper bag"]
    },
    {
        title: "3 Tote Bags Reutilizables para Compras 2025: Sostenibilidad y Estilo",
        description: "Descubre las 3 mejores tote bags reutilizables para compras 2025. Guía completa con reseñas detalladas, comparativas y enlaces de compra para reducir tu huella ambiental mientras mantienes el estilo.",
        category: "Tote Bags",
        url: "/articulos/3-tote-bags-reutilizables-compras-2025.html",
        image: "../photos/Nook%20Theory%20Reusable%20Insulated%20Grocery%20Bag%20-%20Leak%20Proof,%20X%20Large%20Insulated%20Cooler%20Bag%20-%20Insulated%20Shopping%20Bags%20for%20Groceries%20-%20Travel%20Cooler%20Bag%20for%20Frozen.jpg",
        date: "30 Enero 2025",
        tags: ["tote bags", "reutilizables", "compras", "sostenible", "ecológico", "2025", "grocery", "aisladas"]
    },
    {
        title: "Mejores Mochilas para Trabajo 2025",
        description: "Encuentra la mochila perfecta para tu jornada laboral. Comodidad, estilo y funcionalidad en una sola opción.",
        category: "Mochilas",
        url: "/articulos/mejores-mochilas-para-trabajo-2025.html",
        image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=250&fit=crop",
        date: "12 Enero 2025",
        tags: ["mochilas", "trabajo", "comodidad", "funcionalidad", "laboral", "2025"]
    },
    {
        title: "Top 5 Carteras para Mujeres Profesionales 2025",
        description: "Selección rápida con foco en durabilidad, organización y precio. Perfectas para la oficina y uso diario.",
        category: "Carteras",
        url: "/articulos/top-5-carteras-mujeres-profesionales-2025.html",
        image: "/assets/images/toughergun-wallet.jpg",
        date: "15 Enero 2025",
        tags: ["carteras", "profesionales", "mujeres", "elegancia", "funcionalidad", "oficina", "2025"]
    }
];

// Sugerencias de búsqueda populares
const popularSearchTerms = [
    "carteras",
    "bolsos de mano",
    "mochilas",
    "trabajo",
    "elegantes",
    "profesionales",
    "lujo",
    "funcionales",
    "comodidad",
    "oficina",
    "bodas",
    "cenas",
    "viajes",
    "guía",
    "ocasiones",
    "2025",
    "novia",
    "clutch",
    "satin",
    "eventos",
    "estilosas",
    "laptop",
    "antirrobo",
    "USB",
    "reutilizables",
    "sostenible",
    "compras",
    "grocery",
    "aisladas",
    "calidad",
    "resistente",
    "durabilidad",
    "protección",
    "organización",
    "versatilidad",
    "TSA",
    "FlexVent"
];

function performSearch(searchTerm) {
    const searchResults = articlesDatabase.filter(article => {
        const searchableText = [
            article.title.toLowerCase(),
            article.description.toLowerCase(),
            article.category.toLowerCase(),
            ...article.tags.map(tag => tag.toLowerCase())
        ].join(' ');
        
        // Búsqueda exacta
        if (searchableText.includes(searchTerm)) {
            return true;
        }
        
        // Búsqueda por palabras individuales
        const searchWords = searchTerm.split(' ').filter(word => word.length > 2);
        const textWords = searchableText.split(' ');
        
        return searchWords.some(searchWord => 
            textWords.some(textWord => textWord.includes(searchWord))
        );
    });
    
    displaySearchResults(searchResults, searchTerm);
}

function displaySearchResults(results, searchTerm) {
    const searchResultsSection = document.getElementById('searchResults');
    const latestArticlesSection = document.getElementById('latestArticles');
    const searchResultsGrid = document.getElementById('searchResultsGrid');
    const resultCount = document.getElementById('resultCount');
    const searchTermSpan = document.getElementById('searchTerm');
    
    if (searchResultsSection && latestArticlesSection && searchResultsGrid) {
        // Actualizar contadores
        resultCount.textContent = results.length;
        searchTermSpan.textContent = searchTerm;
        
        // Limpiar resultados anteriores
        searchResultsGrid.innerHTML = '';
        
        if (results.length > 0) {
            // Crear tarjetas de resultados
            results.forEach(article => {
                const articleCard = createArticleCard(article);
                searchResultsGrid.appendChild(articleCard);
            });
            
            // Mostrar sección de resultados y ocultar artículos recientes
            searchResultsSection.style.display = 'block';
            latestArticlesSection.style.display = 'none';
            
            // Scroll suave a los resultados
            searchResultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            // Mostrar sugerencias de otros artículos cuando no hay resultados
            showAlternativeArticles(searchTerm);
            searchResultsSection.style.display = 'block';
            latestArticlesSection.style.display = 'none';
            
            // Scroll suave a los resultados
            searchResultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
}

function showAlternativeArticles(searchTerm) {
    const searchResultsGrid = document.getElementById('searchResultsGrid');
    const resultCount = document.getElementById('resultCount');
    const searchTermSpan = document.getElementById('searchTerm');
    
    // Obtener artículos alternativos con puntuación de relevancia
    const alternativeArticles = articlesDatabase.map(article => {
        const searchableText = [
            article.title.toLowerCase(),
            article.description.toLowerCase(),
            article.category.toLowerCase(),
            ...article.tags.map(tag => tag.toLowerCase())
        ].join(' ');
        
        let relevanceScore = 0;
        const searchWords = searchTerm.toLowerCase().split(' ').filter(word => word.length > 2);
        
        // Calcular puntuación de relevancia
        searchWords.forEach(word => {
            if (searchableText.includes(word)) {
                relevanceScore += 1;
            }
            // Bonus por coincidencias en título
            if (article.title.toLowerCase().includes(word)) {
                relevanceScore += 2;
            }
            // Bonus por coincidencias en categoría
            if (article.category.toLowerCase().includes(word)) {
                relevanceScore += 1;
            }
        });
        
        return { article, relevanceScore };
    })
    .filter(item => item.relevanceScore > 0)
    .sort((a, b) => b.relevanceScore - a.relevanceScore)
    .slice(0, 4)
    .map(item => item.article);
    
    // Si no hay artículos relacionados, mostrar todos los artículos
    if (alternativeArticles.length === 0) {
        alternativeArticles.push(...articlesDatabase.slice(0, 4));
    }
    
    searchResultsGrid.innerHTML = `
        <div class="no-results-with-suggestions">
            <div class="no-results-message">
                <p>No se encontraron artículos para "<strong>${searchTerm}</strong>"</p>
                <p>Te sugerimos estos artículos relacionados:</p>
            </div>
            <div class="alternative-articles">
                ${alternativeArticles.map(article => `
                    <article class="article-card alternative-article">
                        <div class="article-image">
                            <img src="${article.image}" alt="${article.title}">
                        </div>
                        <div class="article-content">
                            <h3><a href="${article.url}">${article.title}</a></h3>
                            <p>${article.description}</p>
                            <div class="article-meta">
                                <span class="article-date">${article.date}</span>
                                <span class="article-category">${article.category}</span>
                            </div>
                        </div>
                    </article>
                `).join('')}
            </div>
        </div>
    `;
    
    // Actualizar contador para mostrar sugerencias
    resultCount.textContent = alternativeArticles.length;
    searchTermSpan.textContent = 'sugerencias';
}

function createArticleCard(article) {
    const card = document.createElement('article');
    card.className = 'article-card';
    card.innerHTML = `
        <div class="article-image">
            <img src="${article.image}" alt="${article.title}">
        </div>
        <div class="article-content">
            <h3><a href="${article.url}">${article.title}</a></h3>
            <p>${article.description}</p>
            <div class="article-meta">
                <span class="article-date">${article.date}</span>
                <span class="article-category">${article.category}</span>
            </div>
        </div>
    `;
    return card;
}

function showSearchSuggestions(searchTerm) {
    const searchSuggestions = document.getElementById('searchSuggestions');
    if (!searchSuggestions) return;
    
    // Generar sugerencias
    const suggestions = generateSuggestions(searchTerm);
    
    if (suggestions.length > 0) {
        searchSuggestions.innerHTML = '';
        
        // Agregar sugerencias de artículos
        if (suggestions.articles.length > 0) {
            const articleSection = document.createElement('div');
            articleSection.className = 'suggestion-section';
            articleSection.innerHTML = '<h4>Artículos</h4>';
            
            suggestions.articles.forEach(article => {
                const suggestionItem = createArticleSuggestion(article, searchTerm);
                articleSection.appendChild(suggestionItem);
            });
            
            searchSuggestions.appendChild(articleSection);
        }
        
        // Agregar sugerencias de términos populares
        if (suggestions.terms.length > 0) {
            const termsSection = document.createElement('div');
            termsSection.className = 'suggestion-section';
            termsSection.innerHTML = '<h4>Términos populares</h4>';
            
            suggestions.terms.forEach(term => {
                const suggestionItem = createTermSuggestion(term, searchTerm);
                termsSection.appendChild(suggestionItem);
            });
            
            searchSuggestions.appendChild(termsSection);
        }
        
        searchSuggestions.style.display = 'block';
    } else {
        hideSearchSuggestions();
    }
}

function generateSuggestions(searchTerm) {
    const suggestions = {
        articles: [],
        terms: []
    };
    
    // Buscar artículos que coincidan
    articlesDatabase.forEach(article => {
        const searchableText = [
            article.title.toLowerCase(),
            article.description.toLowerCase(),
            article.category.toLowerCase(),
            ...article.tags.map(tag => tag.toLowerCase())
        ].join(' ');
        
        if (searchableText.includes(searchTerm)) {
            suggestions.articles.push(article);
        }
    });
    
    // Buscar términos populares que coincidan
    popularSearchTerms.forEach(term => {
        if (term.toLowerCase().includes(searchTerm) && !suggestions.terms.includes(term)) {
            suggestions.terms.push(term);
        }
    });
    
    // Si no hay sugerencias de artículos, mostrar artículos relacionados
    if (suggestions.articles.length === 0) {
        const searchWords = searchTerm.split(' ').filter(word => word.length > 2);
        articlesDatabase.forEach(article => {
            const searchableText = [
                article.title.toLowerCase(),
                article.description.toLowerCase(),
                article.category.toLowerCase(),
                ...article.tags.map(tag => tag.toLowerCase())
            ].join(' ');
            
            // Verificar si alguna palabra de búsqueda está presente
            const hasRelatedWord = searchWords.some(word => 
                searchableText.includes(word)
            );
            
            if (hasRelatedWord && suggestions.articles.length < 3) {
                suggestions.articles.push(article);
            }
        });
    }
    
    // Limitar resultados
    suggestions.articles = suggestions.articles.slice(0, 3);
    suggestions.terms = suggestions.terms.slice(0, 5);
    
    return suggestions;
}

function createArticleSuggestion(article, searchTerm) {
    const item = document.createElement('div');
    item.className = 'suggestion-item article-suggestion';
    item.innerHTML = `
        <div class="suggestion-image">
            <img src="${article.image}" alt="${article.title}">
        </div>
        <div class="suggestion-content">
            <h5>${highlightSearchTerm(article.title, searchTerm)}</h5>
            <p>${article.category}</p>
        </div>
    `;
    
    item.addEventListener('click', () => {
        window.location.href = article.url;
    });
    
    return item;
}

function createTermSuggestion(term, searchTerm) {
    const item = document.createElement('div');
    item.className = 'suggestion-item term-suggestion';
    item.innerHTML = `
        <div class="suggestion-icon">🔍</div>
        <span>${highlightSearchTerm(term, searchTerm)}</span>
    `;
    
    item.addEventListener('click', () => {
        const searchInput = document.getElementById('searchInput');
        searchInput.value = term;
        performSearch(term);
        hideSearchSuggestions();
    });
    
    return item;
}

function highlightSearchTerm(text, searchTerm) {
    if (!searchTerm) return text;
    
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

function hideSearchSuggestions() {
    const searchSuggestions = document.getElementById('searchSuggestions');
    if (searchSuggestions) {
        searchSuggestions.style.display = 'none';
    }
}

function clearSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResultsSection = document.getElementById('searchResults');
    const latestArticlesSection = document.getElementById('latestArticles');
    
    if (searchInput) {
        searchInput.value = '';
    }
    
    if (searchResultsSection && latestArticlesSection) {
        searchResultsSection.style.display = 'none';
        latestArticlesSection.style.display = 'block';
    }
    
    hideSearchSuggestions();
}

// ===== FILTRADO POR CATEGORÍAS =====
function initCategoryFiltering() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const articleCards = document.querySelectorAll('.article-card');
    
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const category = this.getAttribute('data-category');
                
                // Si es "todos", filtrar en la misma página
                if (category === 'todos') {
                    // Remover clase active de todos los botones
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    
                    // Agregar clase active al botón clickeado
                    this.classList.add('active');
                    
                    // Filtrar artículos
                    filterArticlesByCategory(category, articleCards);
                } else {
                    // Para otras categorías, navegar a la página dedicada
                    navigateToCategoryPage(category);
                }
            });
        });
    }
}

function navigateToCategoryPage(category) {
    const categoryPages = {
        'bolsos-de-mano': '/articulos/bolsos-de-mano.html',
        'mochilas': '/articulos/mochilas.html',
        'carteras': '/articulos/carteras.html',
        'tote-bags': '/articulos/tote-bags.html'
    };
    
    const targetPage = categoryPages[category];
    if (targetPage) {
        window.location.href = targetPage;
    }
}

function filterArticlesByCategory(category, articleCards) {
    let hasResults = false;
    
    articleCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        
        if (category === 'todos' || cardCategory === category) {
            card.style.display = 'block';
            card.style.animation = 'fadeInUp 0.3s ease-out';
            hasResults = true;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Mostrar mensaje si no hay resultados para la categoría
    if (!hasResults && category !== 'todos') {
        showNoCategoryResults(category);
    }
}

function showNoCategoryResults(category) {
    const articlesGrid = document.querySelector('.articles-grid');
    let noResultsMsg = document.getElementById('no-category-results');
    
    if (!noResultsMsg) {
        noResultsMsg = document.createElement('div');
        noResultsMsg.id = 'no-category-results';
        noResultsMsg.className = 'no-results';
        noResultsMsg.innerHTML = `
            <p>No hay artículos disponibles en la categoría "${category}"</p>
            <p>Prueba con otra categoría o vuelve a "Todos"</p>
        `;
        articlesGrid.appendChild(noResultsMsg);
    } else {
        noResultsMsg.style.display = 'block';
    }
}

function showNoResultsMessage(hasResults, searchTerm) {
    let noResultsMsg = document.getElementById('no-results-message');
    
    if (!hasResults && searchTerm) {
        if (!noResultsMsg) {
            noResultsMsg = document.createElement('div');
            noResultsMsg.id = 'no-results-message';
            noResultsMsg.className = 'no-results';
            noResultsMsg.innerHTML = `
                <p>No se encontraron artículos para "${searchTerm}"</p>
                <p>Intenta con otros términos de búsqueda</p>
            `;
            
            const articlesGrid = document.querySelector('.articles-grid');
            if (articlesGrid) {
                articlesGrid.parentNode.insertBefore(noResultsMsg, articlesGrid.nextSibling);
            }
        }
        noResultsMsg.style.display = 'block';
    } else if (noResultsMsg) {
        noResultsMsg.style.display = 'none';
    }
}

// ===== SCROLL SUAVE =====
function initSmoothScroll() {
    // Scroll suave para enlaces internos
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Ajustar para la navbar fija
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== ENLACES EXTERNOS =====
function initExternalLinks() {
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    
    externalLinks.forEach(link => {
        // Agregar atributos de seguridad para enlaces externos
        link.setAttribute('rel', 'sponsored noopener noreferrer');
        link.setAttribute('target', '_blank');
        
        // Agregar indicador visual para enlaces externos
        if (!link.querySelector('.external-icon')) {
            const icon = document.createElement('span');
            icon.className = 'external-icon';
            icon.innerHTML = ' ↗';
            icon.style.fontSize = '0.8em';
            icon.style.opacity = '0.7';
            link.appendChild(icon);
        }
    });
}

// ===== EFECTOS DE SCROLL =====
function initScrollEffects() {
    // Efecto de navbar al hacer scroll
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Agregar/remover clase para efecto de transparencia
        if (scrollTop > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Ocultar/mostrar navbar al hacer scroll (opcional)
        if (scrollTop > lastScrollTop && scrollTop > 200) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Animación de elementos al hacer scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observar elementos para animación
    const animateElements = document.querySelectorAll('.category-card, .article-card, .section-title');
    animateElements.forEach(el => observer.observe(el));
}

// ===== UTILIDADES ADICIONALES =====

// Función para mostrar/ocultar botón "Volver arriba"
function initBackToTop() {
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '↑';
    backToTopBtn.className = 'back-to-top';
    backToTopBtn.setAttribute('aria-label', 'Volver arriba');
    document.body.appendChild(backToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Función para lazy loading de imágenes
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Función para manejar errores de carga de imágenes
function handleImageErrors() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        img.addEventListener('error', function() {
            this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDQwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRjVGNUJEQyIvPgo8dGV4dCB4PSIyMDAiIHk9IjE1MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE2IiBmaWxsPSIjNjc3NTdEIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+SW1hZ2VuIG5vIGRpc3BvbmlibGU8L3RleHQ+Cjwvc3ZnPgo=';
            this.alt = 'Imagen no disponible';
        });
    });
}

// ===== INICIALIZACIÓN ADICIONAL =====
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades adicionales
    initBackToTop();
    initLazyLoading();
    handleImageErrors();
    
    // Agregar estilos CSS dinámicos para el botón "Volver arriba"
    const style = document.createElement('style');
    style.textContent = `
        .back-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            background-color: var(--color-terracota);
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 20px;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .back-to-top.visible {
            opacity: 1;
            visibility: visible;
        }
        
        .back-to-top:hover {
            background-color: #d4a08c;
            transform: translateY(-2px);
        }
        
        .navbar.scrolled {
            background-color: rgba(255, 255, 255, 0.98);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .animate-in {
            animation: fadeInUp 0.6s ease-out forwards;
        }
        
        .no-results {
            text-align: center;
            padding: 2rem;
            background-color: var(--color-gris-claro);
            border-radius: var(--border-radius);
            margin: 2rem 0;
        }
        
        .no-results p {
            color: var(--color-gris-medio);
            margin-bottom: 0.5rem;
        }
        
        .external-icon {
            display: inline-block;
            margin-left: 0.25rem;
        }
    `;
    document.head.appendChild(style);
});

// ===== MANEJO DE ERRORES =====
window.addEventListener('error', function(e) {
    console.error('Error en la aplicación:', e.error);
});

// ===== PERFORMANCE =====
// Optimizar scroll events con throttling
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Aplicar throttling a eventos de scroll
window.addEventListener('scroll', throttle(function() {
    // Funciones que se ejecutan en scroll
}, 16)); // ~60fps
