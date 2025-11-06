#!/usr/bin/env node

/**
 * Add AdSense script to all HTML pages that don't already have it
 */

import * as cheerio from 'cheerio';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const ADSENSE_SCRIPT = `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8379967738924229"
     crossorigin="anonymous"></script>`;

// Files to skip
const SKIP_FILES = [
  'test-flicker.html',
  'index.html.backup',
  'test-filtering.html'
];

async function walkDir(dir) {
  const files = [];
  const entries = await fs.readdir(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await walkDir(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      files.push(fullPath);
    }
  }
  
  return files;
}

async function addAdSenseToFile(filePath) {
  const content = await fs.readFile(filePath, 'utf8');
  
  // Skip if already has AdSense
  if (content.includes('pagead2.googlesyndication.com')) {
    return { added: false, reason: 'already-has-adsense' };
  }
  
  const $ = cheerio.load(content, { 
    decodeEntities: false,
    xmlMode: false 
  });
  
  const head = $('head');
  if (head.length === 0) {
    return { added: false, reason: 'no-head-tag' };
  }
  
  // Find GTM or first script in head to insert before, or append to head
  const gtmScript = head.find('script').first();
  
  if (gtmScript.length > 0) {
    // Insert before GTM
    gtmScript.before('\n    ' + ADSENSE_SCRIPT);
  } else {
    // Append to head
    head.append('\n    ' + ADSENSE_SCRIPT + '\n');
  }
  
  await fs.writeFile(filePath, $.html(), 'utf8');
  return { added: true };
}

async function main() {
  console.log('🔍 Scanning for HTML files...\n');
  
  const allFiles = await walkDir(ROOT);
  const htmlFiles = allFiles.filter(f => {
    const basename = path.basename(f);
    return !SKIP_FILES.includes(basename);
  });
  
  console.log(`Found ${htmlFiles.length} HTML files to process\n`);
  
  let added = 0;
  let skipped = 0;
  let errors = 0;
  
  for (const file of htmlFiles) {
    const relPath = path.relative(ROOT, file);
    
    try {
      const result = await addAdSenseToFile(file);
      
      if (result.added) {
        console.log(`✅ ${relPath}`);
        added++;
      } else {
        console.log(`⏭️  ${relPath} - ${result.reason}`);
        skipped++;
      }
    } catch (err) {
      console.error(`❌ ${relPath} - ${err.message}`);
      errors++;
    }
  }
  
  console.log(`\n📊 Summary:`);
  console.log(`   ✅ Added: ${added}`);
  console.log(`   ⏭️  Skipped: ${skipped}`);
  console.log(`   ❌ Errors: ${errors}`);
  console.log(`   📄 Total: ${htmlFiles.length}`);
}

main().catch(console.error);

