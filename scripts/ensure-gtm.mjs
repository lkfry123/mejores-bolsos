#!/usr/bin/env node
/**
 * ensure-gtm.mjs
 * Inserts Google Tag Manager (GT-MR24WCXH) snippets and removes conflicting GA/legacy tags
 * across all HTML files. Safe to run repeatedly (idempotent).
 */
import fs from 'fs';
import path from 'path';

const ROOT = process.cwd();
const VALID_GTM = 'GTM-TCG7SMDD';
const VALID_GA4 = 'G-H1Q1KL01RP';

const HEAD_SNIPPET = `<!-- Google Tag Manager -->\n<script>\n(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});\nvar f=d.getElementsByTagName(s)[0], j=d.createElement(s), dl=l!='dataLayer'?'&l='+l:'';\nj.async=true; j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;\nf.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-TCG7SMDD');\n</script>\n<!-- End Google Tag Manager -->`;

const BODY_SNIPPET = `<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src=\"https://www.googletagmanager.com/ns.html?id=GTM-TCG7SMDD\"\nheight=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->`;

/** Regexes for removal of conflicting tags */
const reGtmWrongScript = /https:\/\/www\.googletagmanager\.com\/gtm\.js\?id=((?:GTM|GT)-[A-Z0-9_-]+)/g;
const reGtmWrongNoscript = /https:\/\/www\.googletagmanager\.com\/ns\.html\?id=((?:GTM|GT)-[A-Z0-9_-]+)/g;
const reGa4Loader = /<script[^>]*src=["']https:\/\/www\.googletagmanager\.com\/gtag\/js\?id=G-[A-Z0-9_-]+["'][^>]*><\/script>/gi;
const reUaAnalytics = /https:\/\/www\.google-analytics\.com\/analytics\.js/gi;
const reGa4ConfigAny = /gtag\(\s*'config'\s*,\s*'G-[A-Z0-9_-]+'\s*\);/gi;

const modified = [];
const removed = [];
const skipped = [];

function walk(dir){
  const entries = fs.readdirSync(dir, { withFileTypes:true });
  for (const e of entries){
    if (e.name.startsWith('.git')) continue; // skip VCS
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.isFile() && e.name.endsWith('.html')) processHtml(p);
  }
}

function removeConflicts(html){
  let out = html;
  // Remove wrong GTM loaders
  out = out.replace(reGtmWrongScript, (m, id)=>{
    if (id !== VALID_GTM) { removed.push(`GTM script ${id}`); return ''; }
    return m;
  });
  // Remove wrong GTM noscripts
  out = out.replace(reGtmWrongNoscript, (m, id)=>{
    if (id !== VALID_GTM) { removed.push(`GTM noscript ${id}`); return ''; }
    return m;
  });
  // Remove all GA4 loaders (we will rely on GTM). Safe because GTM owns GA4.
  out = out.replace(reGa4Loader, (m)=>{ removed.push('gtag.js loader'); return ''; });
  // Remove UA analytics.js
  out = out.replace(reUaAnalytics, (m)=>{ removed.push('UA analytics.js'); return ''; });
  // Remove GA4 config calls
  out = out.replace(reGa4ConfigAny, (m)=>{ removed.push('gtag config'); return ''; });
  return out;
}

function ensureGtm(html){
  let out = html;
  const hasCorrectHead = out.includes(`googletagmanager.com/gtm.js?id=${VALID_GTM}`);
  const hasCorrectBody = out.includes(`googletagmanager.com/ns.html?id=${VALID_GTM}`);

  // Insert head snippet right after first <head>
  if (!hasCorrectHead){
    out = out.replace(/<head>/i, match=> `${match}\n    ${HEAD_SNIPPET}\n    <!-- GA4 is configured in GTM (Container ${VALID_GTM}) using Measurement ID ${VALID_GA4} -->\n`);
  }
  // Insert body noscript right after first <body>
  if (!hasCorrectBody){
    out = out.replace(/<body>/i, match=> `${match}\n    ${BODY_SNIPPET}\n`);
  }
  return out;
}

function processHtml(file){
  try {
    const before = fs.readFileSync(file, 'utf8');
    let html = before;
    html = removeConflicts(html);
    html = ensureGtm(html);
    if (html !== before){
      fs.writeFileSync(file, html, 'utf8');
      modified.push(file);
    }
  } catch (e){
    skipped.push(`${file} -> ${e.message}`);
  }
}

walk(ROOT);

// Emit a short report to console and write REPORT.md (append)
const lines = [];
lines.push('# GTM Injection Report');
lines.push('');
lines.push(`- Modified files: ${modified.length}`);
modified.forEach(f=> lines.push(`  - ${path.relative(ROOT,f)}`));
if (removed.length){
  lines.push('- Removed snippets:');
  removed.forEach(r=> lines.push(`  - ${r}`));
}
if (skipped.length){
  lines.push('- Skipped files (errors):');
  skipped.forEach(s=> lines.push(`  - ${s}`));
}
lines.push('');

const reportPath = path.join(ROOT, 'REPORT.md');
try {
  fs.writeFileSync(reportPath, lines.join('\n'), 'utf8');
} catch {}

console.log(lines.join('\n'));

