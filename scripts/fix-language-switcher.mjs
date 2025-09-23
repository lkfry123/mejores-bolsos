#!/usr/bin/env node
import { readdir, readFile, writeFile, stat } from 'fs/promises';
import { join } from 'path';

const PROJECT_ROOT = process.cwd();

async function listHtmlFiles(dir) {
  const out = [];
  async function walk(current) {
    const entries = await readdir(current, { withFileTypes: true });
    for (const entry of entries) {
      const full = join(current, entry.name);
      if (entry.isDirectory()) {
        await walk(full);
      } else if (entry.isFile() && entry.name.endsWith('.html')) {
        out.push(full);
      }
    }
  }
  await walk(dir);
  return out;
}

function toTrailingSlash(url) {
  if (!url.startsWith('https://affordable-handbags.com')) return url;
  // index.html -> /
  url = url.replace(/\/index\.html$/i, '/');
  // .html -> /
  url = url.replace(/\.html$/i, '/');
  return url;
}

function replaceLanguageSwitcher(html, currentLang, enUrl, esUrl) {
  if (!enUrl && !esUrl) return html;
  // Normalize both urls to trailing slash
  if (enUrl) enUrl = toTrailingSlash(enUrl);
  if (esUrl) esUrl = toTrailingSlash(esUrl);

  // Build replacement block preserving minimal structure but fixing hrefs and active class
  // We'll surgically replace hrefs inside the language-switcher div without changing other markup.
  return html.replace(
    /(<!--\s*Language Switcher\s*-->[\s\S]*?<div\s+class=\"language-switcher\"[\s\S]*?>)([\s\S]*?)(<\/div>)/i,
    (m, open, inner, close) => {
      let updated = inner
        // ES link
        .replace(/(<a[^>]*class=(["'])[^\2]*?lang-link[^\2]*?\2[^>]*href=)(["'])([^"']*)(\3)([^>]*>\s*ES\s*<\/a>)/i,
                 (mm, p1, q, q2, href, q3, tail) => {
                   const newHref = esUrl || href;
                   const fixedHref = newHref.replace(/\.html$/i, '/');
                   // ensure active class on ES if currentLang is es
                   let anchor = `${p1}${q2}${fixedHref}${q2}${tail}`;
                   if (currentLang === 'es') {
                     anchor = anchor.replace(/class=(["'])([^"']*)\1/i, (cm, cq, classes) => `class=${cq}${ensureActive(classes)}${cq}`);
                   } else {
                     anchor = anchor.replace(/class=(["'])([^"']*)\1/i, (cm, cq, classes) => `class=${cq}${removeActive(classes)}${cq}`);
                   }
                   return anchor;
                 })
        // EN link
        .replace(/(<a[^>]*class=(["'])[^\2]*?lang-link[^\2]*?\2[^>]*href=)(["'])([^"']*)(\3)([^>]*>\s*EN\s*<\/a>)/i,
                 (mm, p1, q, q2, href, q3, tail) => {
                   const newHref = enUrl || href;
                   const fixedHref = newHref.replace(/\.html$/i, '/');
                   let anchor = `${p1}${q2}${fixedHref}${q2}${tail}`;
                   if (currentLang === 'en') {
                     anchor = anchor.replace(/class=(["'])([^"']*)\1/i, (cm, cq, classes) => `class=${cq}${ensureActive(classes)}${cq}`);
                   } else {
                     anchor = anchor.replace(/class=(["'])([^"']*)\1/i, (cm, cq, classes) => `class=${cq}${removeActive(classes)}${cq}`);
                   }
                   return anchor;
                 });
      // Also remove .html endings in any hrefs within the language switcher as a safeguard
      updated = updated.replace(/(href=)(["'])([^"']+?)\.html(\2)/gi, (mm, p1, q, path, q2) => `${p1}${q}${path}/${q2}`);
      return `${open}${updated}${close}`;
    }
  );
}

function ensureActive(classes) {
  const set = new Set(classes.split(/\s+/).filter(Boolean));
  set.add('active');
  return Array.from(set).join(' ');
}
function removeActive(classes) {
  const set = new Set(classes.split(/\s+/).filter(Boolean));
  set.delete('active');
  return Array.from(set).join(' ');
}

async function processFile(file) {
  const original = await readFile(file, 'utf8');
  let html = original;
  // Detect lang from <html lang="..">
  const langMatch = html.match(/<html[^>]*\blang=(["'])([a-z\-]+)\1/i);
  const currentLang = langMatch ? langMatch[2].toLowerCase() : null;

  // Extract alternate URLs
  const enAlt = (html.match(/<link\s+rel=\"alternate\"[^>]*hreflang=\"en\"[^>]*href=\"([^\"]+)\"/i) || [])[1] || null;
  const esAlt = (html.match(/<link\s+rel=\"alternate\"[^>]*hreflang=\"es\"[^>]*href=\"([^\"]+)\"/i) || [])[1] || null;

  // Replace language switcher
  html = replaceLanguageSwitcher(html, currentLang, enAlt, esAlt);

  if (html !== original) {
    await writeFile(file, html, 'utf8');
    return true;
  }
  return false;
}

(async () => {
  const files = await listHtmlFiles(PROJECT_ROOT);
  let changed = 0;
  for (const file of files) {
    try {
      const did = await processFile(file);
      if (did) changed++;
    } catch (e) {
      console.warn('Skip on error:', file, e.message);
    }
  }
  console.log(`Language switcher fix complete. Files updated: ${changed}`);
})();


