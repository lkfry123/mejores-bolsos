#!/bin/bash

# Add "Take the Quiz" link to navigation menus
# This script adds the quiz link to all HTML files with nav-menu

files=(
    "./affiliate-disclosure.html"
    "./privacy-policy.html"
    "./articles/fun-unique-gift-wallets-2025.html"
    "./articles/travel-light-adventure-bags-2025.html"
    "./articles/wallets.html"
    "./articles/best-lightweight-travel-backpacks-2025.html"
    "./articles/3-functional-diaper-bags-moms-2025.html"
    "./articles/index.html"
    "./articles/minimalist-daily-bag-2025.html"
    "./articles/3-rfid-security-wallets-2025.html"
    "./articles/how-to-choose-perfect-handbag-2025.html"
    "./articles/backpacks.html"
    "./articles/3-reusable-shopping-tote-bags-2025.html"
    "./articles/tote-bags.html"
    "./articles/affordable-elegant-casual-handbags-wedding-guest-2025.html"
    "./articles/handbags.html"
    "./articles/best-wedding-handbags-2025.html"
    "./articles/3-functional-university-tote-bags-2025.html"
    "./articles/3-stylish-professional-backpacks-2025.html"
    "./articles/3-popular-amazon-tote-bags-2025.html"
    "./articles/3-wristlet-wallets-women-2025.html"
    "./articles/top-5-professional-women-wallets-2025.html"
    "./articles/laptop-backpacks-protection-style-2025.html"
    "./articles/best-durable-stylish-backpacks-2025.html"
    "./es/politica-privacidad.html"
    "./es/aviso-afiliados.html"
    "./es/articulos/bolsos-de-mano.html"
    "./es/articulos/mochilas.html"
    "./es/articulos/top-5-carteras-mujeres-profesionales-2025.html"
    "./es/articulos/3-tote-bags-reutilizables-compras-2025.html"
    "./es/articulos/index.html"
    "./es/articulos/bolsos-casual-elegantes-asequibles-invitadas-bodas-2025.html"
    "./es/articulos/mochilas-para-laptop-proteccion-estilo-2025.html"
    "./es/articulos/3-mochilas-profesionales-estilosas-2025.html"
    "./es/articulos/3-tote-bags-populares-amazon-2025.html"
    "./es/articulos/las-mejores-mochilas-mano-viajar-ligero-2025.html"
    "./es/articulos/bolso-minimalista-dia-dia-2025.html"
    "./es/articulos/tote-bags.html"
    "./es/articulos/3-carteras-rfid-seguridad-2025.html"
    "./es/articulos/mejores-bolsos-mano-bodas-2025.html"
    "./es/articulos/3-carteras-wristlet-mujeres-2025.html"
    "./es/articulos/3-bolsos-panales-funcionales-mamas-2025.html"
    "./es/articulos/como-elegir-bolso-mano-perfecto-2025.html"
    "./es/articulos/carteras.html"
    "./es/articulos/viajar-ligera-bolsos-aventureras-2025.html"
    "./es/articulos/3-tote-bags-funcionales-universidad-2025.html"
    "./es/articulos/carteras-divertidas-unicas-regalo-2025.html"
    "./es/articulos/resistentes-estilo-mejores-mochilas-dia-dia-2025.html"
    "./es/articulos/best-durable-stylish-backpacks-2025.html"
    "./es/categorias/carteras/index.html"
    "./es/categorias/index.html"
    "./es/categorias/mochilas/index.html"
    "./es/categorias/tote-bags/index.html"
    "./es/categorias/bolsos-de-mano/index.html"
    "./categories/carteras/index.html"
    "./categories/index.html"
    "./categories/mochilas/index.html"
    "./categories/tote-bags/index.html"
    "./categories/bolsos-de-mano/index.html"
    "./categories/wallets/index.html"
    "./categories/backpacks/index.html"
    "./categories/handbags/index.html"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        # Check if quiz link already exists
        if ! grep -q "quiz/bag-personality" "$file"; then
            # Add quiz link before Contact link
            sed -i '' 's|<li><a href="#contact" class="nav-link">Contact</a></li>|<li><a href="/quiz/bag-personality/" class="nav-link">Take the Quiz</a></li>\n                <li><a href="#contact" class="nav-link">Contact</a></li>|g' "$file"
            sed -i '' 's|<li><a href="#contacto" class="nav-link">Contacto</a></li>|<li><a href="/quiz/bag-personality/" class="nav-link">Take the Quiz</a></li>\n                <li><a href="#contacto" class="nav-link">Contacto</a></li>|g' "$file"
            echo "Updated: $file"
        else
            echo "Skipped: $file (already has quiz link)"
        fi
    fi
done
