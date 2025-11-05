import { promises as fs } from 'fs';
import path from 'path';
import * as cheerio from 'cheerio';

const ORIGIN = 'https://affordable-handbags.com';
const OUT = process.env.OUT_DIR || '.';

const changed = [];
const skipped = [];
const errors = [];

function isHtmlFile(p) { return p.toLowerCase().endsWith('.html'); }

function ensureSlashPathname(pn) {
  const last = pn.split('/').filter(Boolean).pop() || '';
  const looksFile = last.includes('.');
  if (!looksFile && !pn.endsWith('/')) return pn + '/';
  return pn;
}

function fileToPathname(file) {
  // /dist/about/index.html -> /about/
  // /dist/bag.html        -> /bag/
  // about/index.html      -> /about/
  let rel = file;
  
  // If OUT is ".", make path relative to current working directory
  if (OUT === '.') {
    const cwd = process.cwd();
    if (file.startsWith(cwd)) {
      rel = file.slice(cwd.length);
    } else {
      // Try path.relative approach
      rel = path.relative(OUT, file);
    }
  } else {
    // For other OUT directories, use regex replacement
    rel = file.replace(new RegExp(`^${OUT}`), '');
  }
  
  rel = rel.replace(/\\/g, '/');
  if (!rel.startsWith('/')) rel = '/' + rel;
  rel = rel.replace(/\/index\.html$/i, '/');
  rel = rel.replace(/\.html$/i, '/');
  return ensureSlashPathname(rel);
}

function canonicalForFile(file) {
  const pathname = fileToPathname(file);
  return `${ORIGIN}${pathname}`;
}

async function walk(dir) {
  const out = [];
  try {
    const ents = await fs.readdir(dir, { withFileTypes: true });
    for (const e of ents) {
      // Skip node_modules, .git, and other common build artifacts
      if (e.name.startsWith('.') && e.name !== '.') continue;
      if (e.name === 'node_modules') continue;
      if (e.name === 'dist') continue;
      if (e.name === 'build') continue;
      
      const p = path.join(dir, e.name);
      if (e.isDirectory()) {
        out.push(...await walk(p));
      } else if (e.isFile() && isHtmlFile(p)) {
        out.push(p);
      }
    }
  } catch (e) {
    // Skip directories we can't read
  }
  return out;
}

function upsertCanonicalAndOg(html, canon) {
  const $ = cheerio.load(html);

  // Remove all existing canonical tags first, then add one
  $('link[rel="canonical"]').remove();
  $('head').append(`\n<link rel="canonical" href="${canon}">`);

  // og:url: ensure single and matching
  $('meta[property="og:url"]').remove();
  $('head').append(`\n<meta property="og:url" content="${canon}">`);

  return $.html();
}

(async () => {
  try {
    const files = await walk(OUT);
    if (!files.length) {
      console.log(`No HTML files found under ${OUT}. Set OUT_DIR if needed.`);
      process.exit(0);
    }

    for (const file of files) {
      try {
        let html = await fs.readFile(file, 'utf8');

        // Compute self canonical for this file
        let canon = canonicalForFile(file);

        // If page previously pointed canonical to homepage, replace with self
        // (This catches /about/, /contact/, /terms/ mis-canonicals)
        // We rewrite anyway since we remove & re-add clean tags.

        const outHtml = upsertCanonicalAndOg(html, canon);

        if (outHtml !== html) {
          await fs.writeFile(file, outHtml, 'utf8');
          changed.push(file);
        } else {
          skipped.push(file);
        }
      } catch (e) {
        errors.push({ file, error: e.message });
      }
    }

    console.log(`\nFix complete.`);
    console.log(`Changed: ${changed.length} file(s)`);
    console.log(`Unchanged: ${skipped.length} file(s)`);
    if (changed.length) {
      console.log(`\nSample changed file: ${changed[0]}`);
    }
    if (errors.length) {
      console.log(`\nErrors (${errors.length}):`);
      for (const r of errors.slice(0, 10)) {
        console.log(` - ${r.file}: ${r.error}`);
      }
    }
  } catch (e) {
    console.error('Fatal:', e);
    process.exit(1);
  }
})();

