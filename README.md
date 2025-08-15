# Bolsos & Moda - Sitio Web Estático

Un sitio web moderno y elegante dedicado a bolsos, mochilas y accesorios de moda. Diseñado con colores suaves en tonos tierra y pasteles, tipografía limpia y funcionalidades interactivas.

## 🎨 Características del Diseño

- **Paleta de colores suaves**: Beige, arena, terracota, verde oliva y gris claro
- **Tipografía moderna**: Inter (Google Fonts)
- **Diseño responsive**: Optimizado para móvil y escritorio
- **Navegación intuitiva**: Menú fijo con scroll suave
- **Buscador funcional**: Filtrado de artículos en tiempo real
- **SEO optimizado**: Datos estructurados JSON-LD y meta tags

## 📁 Estructura del Proyecto

```
├── index.html                 # Página principal
├── assets/
│   ├── styles.css            # Estilos principales
│   └── script.js             # Funcionalidades JavaScript
├── categorias/
│   └── bolsos-de-mano/
│       └── index.html        # Página de categoría
├── articulos/
│   └── mejores-bolsos-de-mano-2025.html  # Artículo de ejemplo
├── sitemap.xml               # Mapa del sitio
├── robots.txt                # Configuración para crawlers
└── README.md                 # Este archivo
```

## 🚀 Despliegue

### Netlify
1. Conecta tu repositorio de GitHub a Netlify
2. Configura el directorio de build como `/` (raíz)
3. El sitio se desplegará automáticamente

### Vercel
1. Instala Vercel CLI: `npm i -g vercel`
2. Ejecuta `vercel` en el directorio del proyecto
3. Sigue las instrucciones para configurar el dominio

### Cloudflare Pages
1. Ve a Cloudflare Dashboard > Pages
2. Conecta tu repositorio de GitHub
3. Configura el directorio de build como `/`

## 📝 Cómo Añadir Nuevos Artículos

### 1. Crear el archivo HTML del artículo

Crea un nuevo archivo en `/articulos/` con el formato:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Título del Artículo - Bolsos & Moda</title>
    <meta name="description" content="Descripción del artículo para SEO">
    <link rel="stylesheet" href="../assets/styles.css">
    <!-- Datos estructurados JSON-LD -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Título del Artículo",
        "description": "Descripción del artículo",
        "numberOfItems": 10,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "item": {
                    "@type": "Product",
                    "name": "Nombre del Producto",
                    "description": "Descripción del producto",
                    "image": "URL de la imagen",
                    "offers": {
                        "@type": "Offer",
                        "price": "99.99",
                        "priceCurrency": "EUR",
                        "availability": "https://schema.org/InStock"
                    }
                }
            }
        ]
    }
    </script>
</head>
<body>
    <!-- Navegación -->
    <nav class="navbar">
        <!-- Copiar navegación del index.html -->
    </nav>

    <!-- Header del Artículo -->
    <header class="article-header">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/">Inicio</a> > 
                <a href="/categorias/categoria/">Categoría</a> > 
                <span>Título del Artículo</span>
            </nav>
            <h1 class="article-title">Título del Artículo</h1>
            <p class="article-subtitle">Subtítulo descriptivo</p>
            <div class="article-meta">
                <span class="article-date">Fecha</span>
                <span class="article-category">Categoría</span>
                <span class="article-reading-time">Tiempo de lectura: X min</span>
            </div>
        </div>
    </header>

    <!-- Contenido Principal -->
    <main class="article-content">
        <div class="container">
            <div class="content-wrapper">
                <!-- Tabla de Contenido -->
                <aside class="table-of-contents">
                    <h3>Tabla de Contenido</h3>
                    <ul>
                        <li><a href="#introduccion">Introducción</a></li>
                        <!-- Añadir más enlaces según el contenido -->
                    </ul>
                </aside>

                <!-- Contenido del Artículo -->
                <article class="main-content">
                    <section id="introduccion">
                        <h2>Introducción</h2>
                        <p>Contenido de la introducción...</p>
                    </section>

                    <!-- Review de Producto -->
                    <div class="product-review" id="producto-1">
                        <h3>1. Nombre del Producto</h3>
                        <div class="product-image">
                            <img src="URL_DE_LA_IMAGEN" alt="Descripción de la imagen">
                        </div>
                        <div class="product-info">
                            <p class="product-description">Descripción del producto...</p>
                            
                            <div class="pros-cons">
                                <div class="pros">
                                    <h4>✅ Ventajas</h4>
                                    <ul>
                                        <li>Ventaja 1</li>
                                        <li>Ventaja 2</li>
                                    </ul>
                                </div>
                                <div class="cons">
                                    <h4>❌ Desventajas</h4>
                                    <ul>
                                        <li>Desventaja 1</li>
                                        <li>Desventaja 2</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <a href="ENLACE_DE_AFILIADO" class="btn btn-primary" rel="sponsored noopener" target="_blank">Comprar en Amazon</a>
                        </div>
                    </div>

                    <!-- FAQ -->
                    <section id="faq">
                        <h2>Preguntas Frecuentes</h2>
                        <div class="faq-item">
                            <h3>¿Pregunta?</h3>
                            <p>Respuesta...</p>
                        </div>
                    </section>
                </article>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <!-- Copiar footer del index.html -->
    </footer>

    <script src="../assets/script.js"></script>
</body>
</html>
```

### 2. Actualizar la página de categoría

Añade el nuevo artículo a la página de categoría correspondiente en `/categorias/categoria/index.html`:

```html
<article class="article-card">
    <div class="article-image">
        <img src="URL_DE_LA_IMAGEN" alt="Descripción">
    </div>
    <div class="article-content">
        <h3><a href="/articulos/nombre-del-articulo.html">Título del Artículo</a></h3>
        <p>Descripción corta del artículo...</p>
        <div class="article-meta">
            <span class="article-date">Fecha</span>
            <span class="article-category">Categoría</span>
        </div>
    </div>
</article>
```

### 3. Actualizar el sitemap.xml

Añade la nueva URL al sitemap:

```xml
<url>
    <loc>https://tudominio.com/articulos/nombre-del-articulo.html</loc>
    <lastmod>2025-01-XX</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
</url>
```

### 4. Actualizar la página principal (opcional)

Si es un artículo destacado, añádelo a la sección "Últimos Artículos" en `index.html`.

## 🎯 Mejores Prácticas

### SEO
- Usa títulos descriptivos y únicos
- Incluye meta descriptions atractivas
- Optimiza las imágenes con alt text descriptivo
- Usa URLs amigables para SEO
- Incluye datos estructurados JSON-LD

### Contenido
- Escribe contenido original y valioso
- Incluye pros y contras honestos
- Usa imágenes de alta calidad
- Mantén un tono profesional pero accesible
- Incluye enlaces de afiliado relevantes

### Enlaces de Afiliado
- Siempre usa `rel="sponsored noopener"` para enlaces externos
- Incluye el aviso de afiliados en el footer
- Mantén transparencia sobre las comisiones

## 🔧 Personalización

### Cambiar Colores
Edita las variables CSS en `assets/styles.css`:

```css
:root {
    --color-beige: #f5f5dc;
    --color-arena: #f4e4bc;
    --color-terracota: #e8b4a0;
    /* ... más colores */
}
```

### Añadir Nuevas Categorías
1. Crea el directorio en `/categorias/nueva-categoria/`
2. Crea `index.html` para la categoría
3. Actualiza la navegación en todas las páginas
4. Añade al sitemap.xml

### Modificar Funcionalidades
Edita `assets/script.js` para personalizar:
- Comportamiento del buscador
- Efectos de scroll
- Animaciones
- Funcionalidades móviles

## 📊 Analytics y Seguimiento

### Google Analytics
Añade el código de seguimiento en el `<head>` de todas las páginas:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Enlaces de Afiliado
- Amazon Associates
- Otros programas de afiliados relevantes

## 🚨 Aviso Legal

Este sitio utiliza enlaces de afiliado. Podemos recibir una comisión si compras a través de nuestros enlaces. Esto no afecta el precio que pagas por los productos.

## 📞 Soporte

Para preguntas o soporte técnico, contacta a través de:
- Email: contacto@tudominio.com
- GitHub Issues: [Crear un issue](https://github.com/tu-usuario/tu-repo/issues)

---

**Nota**: Recuerda reemplazar `tudominio.com` con tu dominio real en todos los archivos antes del despliegue.
