#!/usr/bin/env node
/**
 * Sitemap Audit Tool
 * Compares all live HTML files against sitemap.xml to find missing pages
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

// Exclude patterns
const EXCLUDE_PATTERNS = [
  /node_modules/,
  /\.git/,
  /tools\//,
  /test-/,
  /\.backup/,
  /sitemap/,
  /robots\.txt/,
];

// Files that should be excluded (test files, etc.)
const EXCLUDE_FILES = [
  'test-flicker.html',
  'tools/cmp-test.html',
  'index.html.backup',
];

/**
 * Convert file path to live URL
 */
function fileToUrl(filePath) {
  // Remove root prefix
  let url = filePath.replace(ROOT, '').replace(/\\/g, '/');
  
  // Remove leading slash
  if (url.startsWith('/')) url = url.slice(1);
  
  // Special case: root index.html
  if (url === 'index.html') {
    return 'https://affordable-handbags.com/';
  }
  
  // Handle index.html files
  if (url.endsWith('/index.html')) {
    url = url.replace('/index.html', '/');
  } else if (url.endsWith('index.html')) {
    url = url.replace('index.html', '');
  } else if (url.endsWith('.html')) {
    // Most .html files redirect to trailing slash (per netlify.toml)
    url = url.replace('.html', '/');
  }
  
  // Ensure trailing slash for directories
  if (!url.endsWith('/') && !url.includes('.')) {
    url += '/';
  }
  
  // Build full URL
  return `https://affordable-handbags.com/${url}`;
}

/**
 * Extract URLs from sitemap.xml
 */
async function extractSitemapUrls() {
  const sitemapPath = path.join(ROOT, 'sitemap.xml');
  const content = await fs.readFile(sitemapPath, 'utf-8');
  
  const urls = [];
  const locRegex = /<loc>(.*?)<\/loc>/g;
  let match;
  
  while ((match = locRegex.exec(content)) !== null) {
    urls.push(match[1].trim());
  }
  
  return new Set(urls);
}

/**
 * Find all HTML files recursively
 */
async function findHtmlFiles(dir = ROOT, files = []) {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.relative(ROOT, fullPath);
      
      // Skip excluded patterns
      if (EXCLUDE_PATTERNS.some(pattern => pattern.test(relativePath))) {
        continue;
      }
      
      // Skip excluded files
      if (EXCLUDE_FILES.some(excluded => relativePath.includes(excluded))) {
        continue;
      }
      
      if (entry.isDirectory()) {
        await findHtmlFiles(fullPath, files);
      } else if (entry.isFile() && entry.name.endsWith('.html')) {
        files.push(fullPath);
      }
    }
    
    return files;
  } catch (err) {
    if (err.code !== 'ENOENT' && err.code !== 'EPERM') {
      console.error(`Error reading ${dir}:`, err.message);
    }
    return files;
  }
}

/**
 * Main audit function
 */
async function main() {
  console.log('🔍 Scanning project for HTML files...\n');
  
  // Get all HTML files
  const htmlFiles = await findHtmlFiles();
  console.log(`Found ${htmlFiles.length} HTML files\n`);
  
  // Convert to URLs
  const liveUrls = new Set();
  const fileToUrlMap = new Map();
  
  for (const file of htmlFiles) {
    const url = fileToUrl(file);
    liveUrls.add(url);
    fileToUrlMap.set(url, path.relative(ROOT, file));
  }
  
  // Get sitemap URLs
  console.log('📋 Reading sitemap.xml...\n');
  const sitemapUrls = await extractSitemapUrls();
  console.log(`Found ${sitemapUrls.size} URLs in sitemap\n`);
  
  // Find missing pages
  const missingFromSitemap = [];
  for (const url of liveUrls) {
    if (!sitemapUrls.has(url)) {
      missingFromSitemap.push({
        url,
        file: fileToUrlMap.get(url),
      });
    }
  }
  
  // Find URLs in sitemap that don't have corresponding files (orphaned)
  const orphanedSitemapUrls = [];
  for (const url of sitemapUrls) {
    if (!liveUrls.has(url)) {
      orphanedSitemapUrls.push(url);
    }
  }
  
  // Generate report
  console.log('='.repeat(80));
  console.log('SITEMAP AUDIT REPORT');
  console.log('='.repeat(80));
  console.log(`\n📊 Summary:`);
  console.log(`   • Total HTML files found: ${htmlFiles.length}`);
  console.log(`   • Live URLs generated: ${liveUrls.size}`);
  console.log(`   • URLs in sitemap: ${sitemapUrls.size}`);
  console.log(`   • Missing from sitemap: ${missingFromSitemap.length}`);
  console.log(`   • Orphaned sitemap URLs: ${orphanedSitemapUrls.length}`);
  
  if (missingFromSitemap.length > 0) {
    console.log(`\n❌ PAGES MISSING FROM SITEMAP (${missingFromSitemap.length}):`);
    console.log('-'.repeat(80));
    
    // Group by category
    const categories = {
      'English Articles': [],
      'Spanish Articles': [],
      'English Categories': [],
      'Spanish Categories': [],
      'Main Pages': [],
      'Other': [],
    };
    
    for (const item of missingFromSitemap) {
      const { url, file } = item;
      if (url.includes('/articles/') && !url.includes('/es/')) {
        categories['English Articles'].push(item);
      } else if (url.includes('/es/articulos/')) {
        categories['Spanish Articles'].push(item);
      } else if (url.includes('/categories/') && !url.includes('/es/')) {
        categories['English Categories'].push(item);
      } else if (url.includes('/es/categorias/')) {
        categories['Spanish Categories'].push(item);
      } else if (url === 'https://affordable-handbags.com/' || 
                 url.includes('/about/') || 
                 url.includes('/contact/') || 
                 url.includes('/terms/') ||
                 url.includes('/privacy-policy/') ||
                 url.includes('/affiliate-disclosure/') ||
                 url.includes('/quiz/') ||
                 url.includes('/search/')) {
        categories['Main Pages'].push(item);
      } else {
        categories['Other'].push(item);
      }
    }
    
    for (const [category, items] of Object.entries(categories)) {
      if (items.length > 0) {
        console.log(`\n${category}:`);
        for (const item of items) {
          console.log(`   • ${item.url}`);
          console.log(`     File: ${item.file}`);
        }
      }
    }
  } else {
    console.log(`\n✅ All live pages are in sitemap!`);
  }
  
  if (orphanedSitemapUrls.length > 0) {
    console.log(`\n⚠️  ORPHANED SITEMAP URLs (${orphanedSitemapUrls.length}):`);
    console.log('   (URLs in sitemap but no corresponding file found)');
    console.log('-'.repeat(80));
    for (const url of orphanedSitemapUrls) {
      console.log(`   • ${url}`);
    }
  }
  
  console.log('\n' + '='.repeat(80));
  
  // Write detailed report to file
  const reportPath = path.join(ROOT, 'SITEMAP-AUDIT-REPORT.md');
  let report = `# Sitemap Audit Report\n\n`;
  report += `Generated: ${new Date().toISOString()}\n\n`;
  report += `## Summary\n\n`;
  report += `- Total HTML files found: ${htmlFiles.length}\n`;
  report += `- Live URLs generated: ${liveUrls.size}\n`;
  report += `- URLs in sitemap: ${sitemapUrls.size}\n`;
  report += `- Missing from sitemap: ${missingFromSitemap.length}\n`;
  report += `- Orphaned sitemap URLs: ${orphanedSitemapUrls.length}\n\n`;
  
  if (missingFromSitemap.length > 0) {
    report += `## Pages Missing from Sitemap\n\n`;
    for (const item of missingFromSitemap) {
      report += `### ${item.url}\n\n`;
      report += `- File: \`${item.file}\`\n`;
      report += `- URL: ${item.url}\n\n`;
    }
  }
  
  if (orphanedSitemapUrls.length > 0) {
    report += `## Orphaned Sitemap URLs\n\n`;
    for (const url of orphanedSitemapUrls) {
      report += `- ${url}\n`;
    }
  }
  
  await fs.writeFile(reportPath, report);
  console.log(`\n📄 Detailed report saved to: SITEMAP-AUDIT-REPORT.md\n`);
}

main().catch(console.error);

