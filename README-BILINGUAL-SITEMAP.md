# Bilingual Sitemap Policy

## Overview
This document outlines the sitemap policy for the bilingual static site `affordable-handbags.com` with English (default) and Spanish (`/es/`) versions.

## URL Structure
- **Canonical domain**: `https://affordable-handbags.com`
- **English pages**: Root paths (e.g., `/articles/wallets/`)
- **Spanish pages**: `/es/` prefix (e.g., `/es/articulos/carteras/`)

## URL Policy Requirements
All URLs in the sitemap must:
- ✅ Use `https://` protocol
- ✅ Use `affordable-handbags.com` domain (no `www`)
- ✅ End with trailing slash `/`
- ✅ No `.html` extensions
- ✅ Follow consistent naming patterns

## Sitemap Structure

### English Pages (Root Paths)
- **Homepage**: `https://affordable-handbags.com/`
- **Legal pages**: 
  - `https://affordable-handbags.com/privacy-policy/`
  - `https://affordable-handbags.com/affiliate-disclosure/`
- **Quiz page**: `https://affordable-handbags.com/quiz/bag-personality/`
- **Category pages**: `https://affordable-handbags.com/categories/[category]/`
- **Article index**: `https://affordable-handbags.com/articles/`
- **Individual articles**: `https://affordable-handbags.com/articles/[article-name]/`

### Spanish Pages (`/es/` Paths)
- **Homepage**: `https://affordable-handbags.com/es/`
- **Legal pages**:
  - `https://affordable-handbags.com/es/politica-privacidad/`
  - `https://affordable-handbags.com/es/aviso-afiliados/`
- **Category pages**: `https://affordable-handbags.com/es/categorias/[category]/`
- **Article index**: `https://affordable-handbags.com/es/articulos/`
- **Individual articles**: `https://affordable-handbags.com/es/articulos/[article-name]/`

## Canonical and Hreflang Tags

### English Pages
```html
<link rel="canonical" href="https://affordable-handbags.com/[path]/">
<link rel="alternate" hreflang="en" href="https://affordable-handbags.com/[path]/">
<link rel="alternate" hreflang="es" href="https://affordable-handbags.com/es/[spanish-path]/">
<link rel="alternate" hreflang="x-default" href="https://affordable-handbags.com/">
```

### Spanish Pages
```html
<link rel="canonical" href="https://affordable-handbags.com/es/[path]/">
<link rel="alternate" hreflang="es" href="https://affordable-handbags.com/es/[path]/">
<link rel="alternate" hreflang="en" href="https://affordable-handbags.com/[english-path]/">
<link rel="alternate" hreflang="x-default" href="https://affordable-handbags.com/">
```

## Robots.txt
```
User-agent: *
Allow: /
Sitemap: https://affordable-handbags.com/sitemap.xml
```

## Sitemap Priorities
- **Homepage**: 1.0 (highest)
- **Language homepages**: 0.9
- **Category/Article indexes**: 0.8
- **Individual articles**: 0.8
- **Category pages**: 0.7
- **Quiz page**: 0.7
- **Legal pages**: 0.3 (lowest)

## Change Frequency
- **Homepage**: weekly
- **Category/Article indexes**: weekly
- **Individual articles**: monthly
- **Category pages**: monthly
- **Legal pages**: monthly

## Maintenance
- Update `lastmod` dates when content changes
- Ensure all new pages are added to sitemap
- Verify canonical and hreflang tags are reciprocal
- Test URLs return 200 status codes
- Validate sitemap XML format

## Testing
Use these commands to verify sitemap URLs:
```bash
# Test English homepage
curl -I https://affordable-handbags.com/

# Test Spanish homepage  
curl -I https://affordable-handbags.com/es/

# Test article pages
curl -I https://affordable-handbags.com/articles/wallets/
curl -I https://affordable-handbags.com/es/articulos/carteras/

# Validate sitemap
curl -I https://affordable-handbags.com/sitemap.xml
```

## File Locations
- **Sitemap**: `/sitemap.xml`
- **Robots**: `/robots.txt`
- **English pages**: Root directory and subdirectories
- **Spanish pages**: `/es/` directory and subdirectories
