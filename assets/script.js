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

// Function to get articles database based on current language
function getArticlesDatabase() {
    const currentPath = window.location.pathname;
    
    // Spanish articles database
    const spanishArticles = [
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
                    url: "/articulos/como-elegir-bolso-mano-perfecto-2025.html",
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
        title: "Top 5 Carteras para Mujeres Profesionales 2025",
        description: "Selección rápida con foco en durabilidad, organización y precio. Perfectas para la oficina y uso diario.",
        category: "Carteras",
        url: "/articulos/top-5-carteras-mujeres-profesionales-2025.html",
        image: "/assets/images/toughergun-wallet.jpg",
        date: "15 Enero 2025",
        tags: ["carteras", "profesionales", "mujeres", "elegancia", "funcionalidad", "oficina", "2025"]
    },
    {
        title: "Bolsos Casual Elegantes y Asequibles Perfectos para Invitadas de Boda 2025",
        description: "Descubre los mejores bolsos casual elegantes y asequibles perfectos para invitadas de boda. Guía completa con reseñas detalladas y enlaces de compra para opciones elegantes y económicas.",
        category: "Bolsos de Mano",
        url: "/articulos/bolsos-casual-elegantes-asequibles-invitadas-bodas-2025.html",
        image: "/photos/KKXIU Women Faux Leather Envelope Clutch Purse Foldover Bags.jpg",
        date: "18 Septiembre 2025",
        tags: ["bolsos de mano", "invitadas de boda", "asequibles", "elegantes", "casual", "clutch", "económicos", "2025"]
    }
    ];

    // English articles database
    const englishArticles = [
        {
            title: "How to Choose the Perfect Handbag 2025",
            description: "Discover how to select the ideal bag according to the occasion. From special events to daily life, we guide you to find the perfect option that combines style, functionality and versatility.",
            category: "Handbags",
            url: "/articles/how-to-choose-perfect-handbag-2025.html",
            image: "/photos/The Sak Sequoia Women's Hobo Handbag Purse.jpg",
            date: "January 15, 2025",
            tags: ["handbags", "guide", "occasions", "style", "functionality", "versatility", "2025"]
        },
        {
            title: "3 Stylish Professional Backpacks 2025",
            description: "Discover the best professional backpacks that combine elegance and functionality. Perfect for work, travel, and everyday use with modern designs and practical features.",
            category: "Backpacks",
            url: "/articles/3-stylish-professional-backpacks-2025.html",
            image: "/photos/LOVEVOOK Laptop Backpack for Women 15.6in Computer Backpacks Dark Green.jpg",
            date: "January 12, 2025",
            tags: ["backpacks", "professional", "elegant", "functional", "work", "travel", "2025"]
        },
        {
            title: "Top 5 Professional Women Wallets 2025",
            description: "Choosing the right wallet not only adds style, it also provides organization and durability. Here we present our recommendations based on functionality, price and elegance.",
            category: "Wallets",
            url: "/articles/top-5-professional-women-wallets-2025.html",
            image: "/photos/COACH Small Wristlet.jpg",
            date: "January 15, 2025",
            tags: ["wallets", "professional", "women", "elegance", "functionality", "office", "2025"]
        },
        {
            title: "Best Durable and Stylish Backpacks 2025",
            description: "Discover why investing in a high-quality backpack is essential. Complete guide with the best durable and stylish backpacks for daily use.",
            category: "Backpacks",
            url: "/articles/best-durable-stylish-backpacks-2025.html",
            image: "/photos/LOVEVOOK Laptop Backpack for Women 15.6in Computer Backpacks Dark Green.jpg",
            date: "January 30, 2025",
            tags: ["backpacks", "quality", "durable", "daily use", "durability", "protection", "comfort", "organization", "versatility", "2025"]
        },
        {
            title: "Best Lightweight Travel Backpacks 2025",
            description: "Perfect for adventure and travel. Lightweight, spacious and with all the necessary compartments for your trips.",
            category: "Backpacks",
            url: "/articles/best-lightweight-travel-backpacks-2025.html",
            image: "/photos/LOVEVOOK Laptop Backpack for Women 15.6in Computer Backpacks Dark Green.jpg",
            date: "January 25, 2025",
            tags: ["backpacks", "travel", "lightweight", "adventure", "spacious", "compartments", "2025"]
        },
        {
            title: "Best Wedding Handbags 2025",
            description: "Discover the 3 best handbags for weddings 2025. Complete guide with detailed reviews, comparisons and purchase links to find the perfect bag for your special day.",
            category: "Handbags",
            url: "/articles/best-wedding-handbags-2025.html",
            image: "/photos/CHARMING TAILOR Classic Satin Clutch Bag Handbag.jpg",
            date: "January 30, 2025",
            tags: ["handbags", "weddings", "clutch", "elegant", "satin", "2025", "bride", "events"]
        },
        {
            title: "Fun and Unique Gift Wallets 2025",
            description: "Perfect gifts for any occasion. Unique and fun wallet designs that will surprise your loved ones.",
            category: "Wallets",
            url: "/articles/fun-unique-gift-wallets-2025.html",
            image: "/photos/COACH Small Wristlet.jpg",
            date: "January 20, 2025",
            tags: ["wallets", "gifts", "unique", "fun", "designs", "surprise", "2025"]
        },
        {
            title: "Minimalist Daily Bag 2025",
            description: "The perfect balance between style and functionality. Minimalist designs for everyday use.",
            category: "Handbags",
            url: "/articles/minimalist-daily-bag-2025.html",
            image: "/photos/The Sak Sequoia Women's Hobo Handbag Purse.jpg",
            date: "January 18, 2025",
            tags: ["handbags", "minimalist", "daily", "style", "functionality", "design", "2025"]
        },
        {
            title: "Travel Light Adventure Bags 2025",
            description: "Essential bags for your adventures. Light, resistant and with all the necessary features for outdoor activities.",
            category: "Backpacks",
            url: "/articles/travel-light-adventure-bags-2025.html",
            image: "/photos/LOVEVOOK Laptop Backpack for Women 15.6in Computer Backpacks Dark Green.jpg",
            date: "January 22, 2025",
            tags: ["backpacks", "travel", "adventure", "light", "resistant", "outdoor", "activities", "2025"]
        },
        {
            title: "Laptop Backpacks: Protection and Style 2025",
            description: "Discover the best laptop backpacks with anti-theft protection, USB ports and TSA design. Complete guide with detailed reviews.",
            category: "Backpacks",
            url: "/articles/laptop-backpacks-protection-style-2025.html",
            image: "/photos/VOLHER Laptop Backpack,Business Travel Anti Theft Slim Durable Laptops Backpack with USB Charging Port,Water Resistant.jpg",
            date: "January 25, 2025",
            tags: ["backpacks", "laptop", "anti-theft", "USB", "TSA", "protection", "2025"]
        },
        {
            title: "3 Popular Amazon Tote Bags 2025",
            description: "Discover the 3 most popular tote bags on Amazon 2025. Complete guide with detailed reviews, comparisons and purchase links.",
            category: "Tote Bags",
            url: "/articles/3-popular-amazon-tote-bags-2025.html",
            image: "/photos/BAGSMART Tote Bag for Women, Foldable Tote Bag With Zipper Travel Large Shoulder Bag Handbag for Work.jpg",
            date: "January 30, 2025",
            tags: ["tote bags", "amazon", "popular", "shopping", "sustainable", "2025"]
        },
        {
            title: "3 Functional Diaper Bags for Moms 2025",
            description: "Discover the 3 best functional diaper bags for moms 2025. Complete guide with detailed reviews, comparisons and purchase links to keep everything organized with your baby.",
            category: "Tote Bags",
            url: "/articles/3-functional-diaper-bags-moms-2025.html",
            image: "/photos/Diaper Bag Tote Large Tote Baby Bag Boy Diaper Bag Stylish Girl Diaper Ba Shoulder Mommy Bag.jpg",
            date: "January 30, 2025",
            tags: ["diaper bags", "moms", "babies", "organization", "functional", "2025", "tote bags"]
        },
        {
            title: "3 Reusable Shopping Tote Bags 2025",
            description: "Discover the 3 best reusable tote bags for shopping 2025. Complete guide with detailed reviews, comparisons and purchase links to reduce your environmental footprint while maintaining style.",
            category: "Tote Bags",
            url: "/articles/3-reusable-shopping-tote-bags-2025.html",
            image: "/photos/Nook Theory Reusable Insulated Grocery Bag - Leak Proof, X Large Insulated Cooler Bag - Insulated Shopping Bags for Groceries - Travel Cooler Bag for Frozen.jpg",
            date: "January 30, 2025",
            tags: ["tote bags", "reusable", "shopping", "sustainable", "eco-friendly", "2025", "grocery", "insulated"]
        },
        {
            title: "3 RFID Security Wallets 2025",
            description: "Protect your cards with RFID blocking technology. Secure and stylish wallets for modern life.",
            category: "Wallets",
            url: "/articles/3-rfid-security-wallets-2025.html",
            image: "/photos/COACH Small Wristlet.jpg",
            date: "January 28, 2025",
            tags: ["wallets", "RFID", "security", "protection", "cards", "technology", "2025"]
        },
        {
            title: "3 Wristlet Wallets for Women 2025",
            description: "Compact and elegant wristlet wallets perfect for essentials. Small but powerful for your daily needs.",
            category: "Wallets",
            url: "/articles/3-wristlet-wallets-women-2025.html",
            image: "/photos/COACH Small Wristlet.jpg",
            date: "January 26, 2025",
            tags: ["wallets", "wristlet", "women", "compact", "elegant", "essentials", "2025"]
        },
        {
            title: "Affordable & Elegant Casual Handbags Perfect for Wedding Guest 2025",
            description: "Discover the best affordable and elegant casual handbags perfect for wedding guests. Complete guide with detailed reviews and purchase links for stylish yet budget-friendly options.",
            category: "Handbags",
            url: "/articles/affordable-elegant-casual-handbags-wedding-guest-2025.html",
            image: "/photos/Y2k Shoulder Bag Red Patent Leather Purse For Women Small Vintage Handbag Burgundy Hobo Bags Faux Leather Underarm1.jpg",
            date: "September 18, 2025",
            tags: ["handbags", "wedding guest", "affordable", "elegant", "casual", "clutch", "budget-friendly", "2025"]
        }
    ];

    // Return appropriate database based on current path
    if (currentPath.startsWith('/es/') || currentPath === '/es' || currentPath === '/es/') {
        return spanishArticles;
    } else {
        return englishArticles;
    }
}

// Get the articles database
const articlesDatabase = getArticlesDatabase();

// Popular search terms based on language
function getPopularSearchTerms() {
    const currentPath = window.location.pathname;
    
    if (currentPath.startsWith('/es/') || currentPath === '/es' || currentPath === '/es/') {
        return [
            "carteras",
            "bolsos de mano",
            "mochilas",
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
            "durabilidad"
        ];
    } else {
        return [
            "handbags",
            "backpacks",
            "wallets",
            "elegant",
            "professional",
            "luxury",
            "functional",
            "comfort",
            "office",
            "weddings",
            "dinners",
            "travel",
            "guide",
            "occasions",
            "2025",
            "bride",
            "clutch",
            "satin",
            "events",
            "stylish",
            "laptop",
            "anti-theft",
            "USB",
            "reusable",
            "sustainable",
            "shopping",
            "grocery",
            "insulated",
            "quality",
            "durable",
            "durability"
        ];
    }
}

// Get popular search terms based on current language
const popularSearchTerms = getPopularSearchTerms();

function performSearch(searchTerm) {
    const currentDatabase = getArticlesDatabase();
    const searchResults = currentDatabase.filter(article => {
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
    const currentDatabase = getArticlesDatabase();
    const alternativeArticles = currentDatabase.map(article => {
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
        alternativeArticles.push(...currentDatabase.slice(0, 4));
    }
    
    searchResultsGrid.innerHTML = `
        <div class="no-results-with-suggestions">
            <div class="no-results-message">
                <p>${window.location.pathname.startsWith('/es/') ? 'No se encontraron artículos para' : 'No articles found for'} "<strong>${searchTerm}</strong>"</p>
                <p>${window.location.pathname.startsWith('/es/') ? 'Te sugerimos estos artículos relacionados:' : 'We suggest these related articles:'}</p>
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
            articleSection.innerHTML = `<h4>${window.location.pathname.startsWith('/es/') ? 'Artículos' : 'Articles'}</h4>`;
            
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
            termsSection.innerHTML = `<h4>${window.location.pathname.startsWith('/es/') ? 'Términos populares' : 'Popular terms'}</h4>`;
            
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
    const currentDatabase = getArticlesDatabase();
    currentDatabase.forEach(article => {
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
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const category = this.getAttribute('data-category');
                
                // Remover clase active de todos los botones
                filterButtons.forEach(btn => btn.classList.remove('active'));
                
                // Agregar clase active al botón clickeado
                this.classList.add('active');
                
                // Filtrar artículos en la misma página
                filterArticlesByCategory(category, articleCards);
                
                return false;
            });
        });
    }
}

function filterArticlesByCategory(category, articleCards) {
    let hasResults = false;
    
    // Función para mostrar animación de fade in
    function showCard(card) {
        card.style.display = 'block';
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 10);
    }

    // Función para ocultar tarjeta
    function hideCard(card) {
        card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.display = 'none';
        }, 300);
    }
    
    articleCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        
        if (category === 'todos' || cardCategory === category) {
            showCard(card);
            hasResults = true;
        } else {
            hideCard(card);
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
