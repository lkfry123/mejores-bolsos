#!/usr/bin/env node
/**
 * Add AdSense script to all HTML files that are missing it.
 * - Do NOT duplicate if already present
 * - Insert strictly between <head></head>, as close to </head> as possible
 * - Preserve paths; do not modify any other content
 */
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const ADS_SNIPPET = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8379967738924229"\n\n     crossorigin="anonymous"></script>';
const ADS_MARKER = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8379967738924229';

async function* walk(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    if (entry.name === 'node_modules') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walk(full);
    } else if (entry.isFile()) {
      yield full;
    }
  }
}

function hasAdSense(html) {
  return html.includes(ADS_MARKER);
}

function insertIntoHead(html) {
  // Find a closing </head> (case-insensitive)
  const match = html.match(/<\/head>/i);
  if (!match) return null;
  const idx = match.index;
  if (idx == null) return null;

  // Determine newline style
  const hasCRLF = html.includes('\r\n');
  const NL = hasCRLF ? '\r\n' : '\n';

  // Insert snippet immediately before </head>, keeping a preceding newline for clarity
  const before = html.slice(0, idx);
  const after = html.slice(idx);
  // If there's already a newline before </head>, keep it minimal
  const needsLeadingNL = before.endsWith(NL) ? '' : NL;
  const insertion = `${needsLeadingNL}${ADS_SNIPPET}${NL}`;
  return before + insertion + after;
}

async function main() {
  const changed = [];
  const skipped = [];

  for await (const file of walk(ROOT)) {
    if (!file.endsWith('.html')) continue;
    // Avoid modifying files under tools/ or scripts/ etc.
    const rel = path.relative(ROOT, file).replace(/\\/g, '/');
    if (rel.startsWith('tools/') || rel.startsWith('scripts/')) continue;

    const html = await fs.readFile(file, 'utf8');
    if (hasAdSense(html)) {
      skipped.push(rel);
      continue;
    }
    const updated = insertIntoHead(html);
    if (updated) {
      await fs.writeFile(file, updated, 'utf8');
      changed.push(rel);
    } else {
      skipped.push(rel);
    }
  }

  console.log(JSON.stringify({ changed, skipped }, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});


