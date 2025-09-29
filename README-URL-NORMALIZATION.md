# URL Normalization Policy

## Overview
This document outlines the URL normalization policy for affordable-handbags.com to ensure consistent, SEO-friendly URLs with proper redirects.

## Canonical URLs
- **English**: `https://affordable-handbags.com/articles/wallets/`
- **Spanish**: `https://affordable-handbags.com/es/articulos/carteras/`

## Redirect Rules
The `_redirects` file contains the following rules in order:

1. **Force HTTPS + apex (final)**
   - `http://affordable-handbags.com/*` → `https://affordable-handbags.com/:splat` 301!
   - `http://www.affordable-handbags.com/*` → `https://affordable-handbags.com/:splat` 301!
   - `https://www.affordable-handbags.com/*` → `https://affordable-handbags.com/:splat` 301!

2. **Normalize .html and /index.html → trailing slash (final)**
   - `/*/index.html` → `/:splat/` 301!
   - `/:page.html` → `/:page/` 301!
   - `/es/*/index.html` → `/es/:splat/` 301!
   - `/es/:page.html` → `/es/:page/` 301!

3. **Don't touch assets**
   - `/*.{xml,json,txt,webmanifest,ico,png,jpg,jpeg,webp,avif,svg,css,js,mp4}` → 200

4. **Quiz page serve**
   - `/quiz/bag-personality/` → `/quiz/bag-personality/index.html` 200

## Why the Order Prevents Multi-hop Chains

The `!` flag in Netlify redirects forces the redirect to be processed immediately, preventing further redirect processing. The order ensures:

1. **HTTPS/apex normalization** happens first** - ensures all traffic goes to the canonical domain
2. **HTML to slash normalization** happens second** - converts .html URLs to trailing slash URLs
3. **Asset protection** happens last** - prevents redirects on static assets

## Testing with curl -I

Use these commands to test redirect behavior:

```bash
# Test .html → slash redirect (should be 301 → 200)
curl -I http://affordable-handbags.com/articles/wallets.html
curl -I https://www.affordable-handbags.com/articles/wallets.html

# Test final URL (should be 200, no redirects)
curl -I https://affordable-handbags.com/articles/wallets/

# Test Spanish version
curl -I https://affordable-handbags.com/es/articulos/carteras.html
curl -I https://affordable-handbags.com/es/articulos/carteras/
```

## Expected Results
- `.html` URLs should redirect with **exactly ONE 301** to the trailing slash version
- Final URLs should return **200** with no redirects
- No redirect chains should occur

## Files Modified
- `_redirects` - Main redirect rules
- `netlify.toml` - Specific redirect for wallets.html
- `sitemap.xml` - Contains canonical URLs
- `robots.txt` - Advertises sitemap
- `articles/wallets.html` - Canonical URL already correct
