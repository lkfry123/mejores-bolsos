// ===== FUNCIONALIDADES PRINCIPALES =====

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todas las funcionalidades
    initMobileMenu();
    initSearchFunctionality();
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
    const articleCards = document.querySelectorAll('.article-card');
    
    if (searchInput && searchBtn) {
        // Búsqueda al escribir
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            filterArticles(searchTerm, articleCards);
        });
        
        // Búsqueda al hacer clic en el botón
        searchBtn.addEventListener('click', function() {
            const searchTerm = searchInput.value.toLowerCase().trim();
            filterArticles(searchTerm, articleCards);
        });
        
        // Búsqueda al presionar Enter
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const searchTerm = this.value.toLowerCase().trim();
                filterArticles(searchTerm, articleCards);
            }
        });
    }
}

function filterArticles(searchTerm, articleCards) {
    let hasResults = false;
    
    articleCards.forEach(card => {
        const title = card.querySelector('h3 a').textContent.toLowerCase();
        const description = card.querySelector('p').textContent.toLowerCase();
        const category = card.querySelector('.article-category').textContent.toLowerCase();
        
        const matches = title.includes(searchTerm) || 
                       description.includes(searchTerm) || 
                       category.includes(searchTerm);
        
        if (matches) {
            card.style.display = 'block';
            card.style.animation = 'fadeInUp 0.3s ease-out';
            hasResults = true;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Mostrar mensaje si no hay resultados
    showNoResultsMessage(hasResults, searchTerm);
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
