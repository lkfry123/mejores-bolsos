#!/usr/bin/env node

import { readdir, stat, writeFile } from 'fs/promises';
import { execSync } from 'child_process';
import { join, extname } from 'path';

const BASE_URL = 'https://affordable-handbags.com';
const PROJECT_ROOT = process.cwd();

/**
 * Get the last git commit date for a file in ISO 8601 format (YYYY-MM-DD)
 */
function getGitLastMod(filePath) {
  try {
    const result = execSync(`git log -1 --format="%cd" --date=iso-strict -- "${filePath}"`, {
      encoding: 'utf8',
      cwd: PROJECT_ROOT
    }).trim();
    // Extract just the date part (YYYY-MM-DD) from the ISO timestamp
    return result.split('T')[0];
  } catch (error) {
    console.warn(`Warning: Could not get git date for ${filePath}, using current date`);
    return new Date().toISOString().split('T')[0];
  }
}

/**
 * Generate sitemap XML content
 */
function generateSitemap(urls) {
  const xmlHeader = '<?xml version="1.0" encoding="UTF-8"?>';
  const urlsetOpen = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
  const urlsetClose = '</urlset>';
  
  const urlEntries = urls.map(url => {
    return `    <url>
        <loc>${url.loc}</loc>
        <lastmod>${url.lastmod}</lastmod>
        <changefreq>${url.changefreq}</changefreq>
        <priority>${url.priority}</priority>
    </url>`;
  }).join('\n');
  
  return `${xmlHeader}
${urlsetOpen}
${urlEntries}
${urlsetClose}`;
}

/**
 * Main function to generate sitemap
 */
async function generateSitemapFile() {
  console.log('Generating sitemap.xml...');
  
  const urls = [];
  
  // Add main page
  urls.push({
    loc: `${BASE_URL}/`,
    lastmod: getGitLastMod('index.html'),
    changefreq: 'weekly',
    priority: '1.0'
  });
  
  // Add categories page
  urls.push({
    loc: `${BASE_URL}/categories/`,
    lastmod: getGitLastMod('categories/index.html'),
    changefreq: 'weekly',
    priority: '0.8'
  });
  
  // Add articles index page
  urls.push({
    loc: `${BASE_URL}/articles/`,
    lastmod: getGitLastMod('articles/index.html'),
    changefreq: 'weekly',
    priority: '0.8'
  });
  
  // Add all article files
  try {
    const articlesDir = join(PROJECT_ROOT, 'articles');
    const files = await readdir(articlesDir);
    
    for (const file of files) {
      if (extname(file) === '.html' && file !== 'index.html') {
        const filePath = join('articles', file);
        urls.push({
          loc: `${BASE_URL}/${filePath}`,
          lastmod: getGitLastMod(filePath),
          changefreq: 'monthly',
          priority: '0.8'
        });
      }
    }
  } catch (error) {
    console.error('Error reading articles directory:', error);
  }
  
  // Generate and write sitemap
  const sitemapContent = generateSitemap(urls);
  const sitemapPath = join(PROJECT_ROOT, 'sitemap.xml');
  
  await writeFile(sitemapPath, sitemapContent, 'utf8');
  
  console.log(`✅ Sitemap generated successfully!`);
  console.log(`📄 Total URLs: ${urls.length}`);
  console.log(`🏠 Home page: 1`);
  console.log(`📂 Category pages: 1`);
  console.log(`📝 Articles: ${urls.length - 2}`);
  console.log(`📁 Output: ${sitemapPath}`);
}

// Run the script
generateSitemapFile().catch(error => {
  console.error('Error generating sitemap:', error);
  process.exit(1);
});
