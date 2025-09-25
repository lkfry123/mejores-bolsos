#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Files to skip (assets, feeds, etc.)
const skipExtensions = ['.css', '.js', '.json', '.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif', '.pdf', '.xml'];
const skipFiles = ['sitemap.xml', 'feed.xml', 'robots.txt'];

function shouldSkipFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const basename = path.basename(filePath);
  return skipExtensions.includes(ext) || skipFiles.includes(basename);
}

function normalizeHtmlLinks(content) {
  // Convert internal .html links to slash URLs
  // Match href="path/to/file.html" or href="../path/to/file.html"
  return content.replace(
    /href="([^"]*?)\.html"/g,
    (match, path) => {
      // Skip external URLs
      if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('mailto:') || path.startsWith('tel:')) {
        return match;
      }
      
      // Convert .html to /
      return `href="${path}/"`;
    }
  );
}

function processFile(filePath) {
  if (shouldSkipFile(filePath)) {
    return false;
  }

  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const normalized = normalizeHtmlLinks(content);
    
    if (content !== normalized) {
      fs.writeFileSync(filePath, normalized, 'utf8');
      console.log(`Updated: ${filePath}`);
      return true;
    }
    return false;
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message);
    return false;
  }
}

function walkDirectory(dir) {
  const files = fs.readdirSync(dir);
  let updatedCount = 0;

  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      updatedCount += walkDirectory(filePath);
    } else if (file.endsWith('.html')) {
      if (processFile(filePath)) {
        updatedCount++;
      }
    }
  }

  return updatedCount;
}

// Main execution
const rootDir = process.cwd();
console.log('Normalizing internal .html links to slash URLs...');
const updatedCount = walkDirectory(rootDir);
console.log(`Updated ${updatedCount} files.`);
