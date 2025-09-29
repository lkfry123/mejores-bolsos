#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Get all HTML files
const htmlFiles = [
  './affiliate-disclosure.html',
  './articles/3-functional-diaper-bags-moms-2025.html',
  './articles/3-functional-university-tote-bags-2025.html',
  './articles/3-popular-amazon-tote-bags-2025.html',
  './articles/3-reusable-shopping-tote-bags-2025.html',
  './articles/3-rfid-security-wallets-2025.html',
  './articles/3-stylish-professional-backpacks-2025.html',
  './articles/3-wristlet-wallets-women-2025.html',
  './articles/affordable-elegant-casual-handbags-wedding-guest-2025.html',
  './articles/backpacks.html',
  './articles/best-durable-stylish-backpacks-2025.html',
  './articles/best-lightweight-travel-backpacks-2025.html',
  './articles/best-wedding-handbags-2025.html',
  './articles/fun-unique-gift-wallets-2025.html',
  './articles/handbags.html',
  './articles/how-to-choose-perfect-handbag-2025.html',
  './articles/index.html',
  './articles/laptop-backpacks-protection-style-2025.html',
  './articles/minimalist-daily-bag-2025.html',
  './articles/top-5-professional-women-wallets-2025.html',
  './articles/tote-bags.html',
  './articles/travel-light-adventure-bags-2025.html',
  './articles/wallets.html',
  './categories/backpacks/index.html',
  './categories/bolsos-de-mano/index.html',
  './categories/carteras/index.html',
  './categories/handbags/index.html',
  './categories/index.html',
  './categories/mochilas/index.html',
  './categories/tote-bags/index.html',
  './categories/wallets/index.html',
  './es/articulos/3-bolsos-panales-funcionales-mamas-2025.html',
  './es/articulos/3-carteras-rfid-seguridad-2025.html',
  './es/articulos/3-carteras-wristlet-mujeres-2025.html',
  './es/articulos/3-mochilas-profesionales-estilosas-2025.html',
  './es/articulos/3-tote-bags-funcionales-universidad-2025.html',
  './es/articulos/3-tote-bags-populares-amazon-2025.html',
  './es/articulos/3-tote-bags-reutilizables-compras-2025.html',
  './es/articulos/best-durable-stylish-backpacks-2025.html',
  './es/articulos/bolso-minimalista-dia-dia-2025.html',
  './es/articulos/bolsos-casual-elegantes-asequibles-invitadas-bodas-2025.html',
  './es/articulos/bolsos-de-mano.html',
  './es/articulos/carteras-divertidas-unicas-regalo-2025.html',
  './es/articulos/carteras.html',
  './es/articulos/como-elegir-bolso-mano-perfecto-2025.html',
  './es/articulos/index.html',
  './es/articulos/las-mejores-mochilas-mano-viajar-ligero-2025.html',
  './es/articulos/mejores-bolsos-mano-bodas-2025.html',
  './es/articulos/mochilas-para-laptop-proteccion-estilo-2025.html',
  './es/articulos/mochilas.html',
  './es/articulos/resistentes-estilo-mejores-mochilas-dia-dia-2025.html',
  './es/articulos/top-5-carteras-mujeres-profesionales-2025.html',
  './es/articulos/tote-bags.html',
  './es/articulos/viajar-ligera-bolsos-aventureras-2025.html',
  './es/aviso-afiliados.html',
  './es/categorias/bolsos-de-mano/index.html',
  './es/categorias/carteras/index.html',
  './es/categorias/index.html',
  './es/categorias/mochilas/index.html',
  './es/categorias/tote-bags/index.html',
  './es/index.html',
  './es/politica-privacidad.html',
  './index.html',
  './privacy-policy.html',
  './quiz/bag-personality/index.html'
];

function convertToFinalUrl(filePath) {
  // Remove leading ./
  let path = filePath.replace(/^\.\//, '');
  
  // Handle index.html files
  if (path.endsWith('/index.html')) {
    path = path.replace('/index.html', '/');
  }
  // Handle other .html files
  else if (path.endsWith('.html')) {
    path = path.replace('.html', '/');
  }
  
  // Ensure trailing slash
  if (!path.endsWith('/')) {
    path += '/';
  }
  
  // Convert to final URL
  return `https://affordable-handbags.com/${path}`;
}

function classifyUrl(url) {
  if (url.includes('/es/')) {
    return 'ES';
  } else {
    return 'EN';
  }
}

// Process all files
const inventory = htmlFiles.map(file => {
  const finalUrl = convertToFinalUrl(file);
  const language = classifyUrl(finalUrl);
  return {
    file,
    finalUrl,
    language
  };
});

// Separate by language
const englishUrls = inventory.filter(item => item.language === 'EN');
const spanishUrls = inventory.filter(item => item.language === 'ES');

console.log('=== INVENTORY RESULTS ===');
console.log(`Total HTML files: ${inventory.length}`);
console.log(`English URLs: ${englishUrls.length}`);
console.log(`Spanish URLs: ${spanishUrls.length}`);
console.log('');

console.log('=== ENGLISH URLS ===');
englishUrls.forEach(item => {
  console.log(`${item.file} → ${item.finalUrl}`);
});

console.log('');
console.log('=== SPANISH URLS ===');
spanishUrls.forEach(item => {
  console.log(`${item.file} → ${item.finalUrl}`);
});

// Export for later use
fs.writeFileSync('inventory.json', JSON.stringify({
  total: inventory.length,
  english: englishUrls.length,
  spanish: spanishUrls.length,
  urls: inventory
}, null, 2));

console.log('');
console.log('Inventory saved to inventory.json');
