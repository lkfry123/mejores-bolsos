import * as cheerio from 'cheerio';
import fs from 'fs/promises';

const ORIGIN = 'https://affordable-handbags.com';
const ENFORCE_TRAILING_SLASH = true;   // your canonical style
const EXPECT_VARIANT_REDIRECTS = true; // per-page redirects in netlify.toml
const MAX_PAGES = 1000;
const MAX_DEPTH = 3;

const visited = new Set();
const toVisit = [{ url: `${ORIGIN}/`, depth: 0 }];
const crawled = new Set();
const fromSitemap = new Set();

const sleep = ms => new Promise(r=>setTimeout(r, ms));

function normalize(u) {
  const x = new URL(u, ORIGIN);
  x.hash = ''; x.search = '';
  const last = x.pathname.split('/').filter(Boolean).pop() || '';
  const looksLikeFile = last.includes('.');
  if (ENFORCE_TRAILING_SLASH && !looksLikeFile && !x.pathname.endsWith('/')) x.pathname += '/';
  if (!ENFORCE_TRAILING_SLASH && x.pathname.endsWith('/') && x.pathname !== '/') x.pathname = x.pathname.slice(0, -1);
  return x.toString();
}

const sameNorm = (a,b) => normalize(a) === normalize(b);
const isInternal = u => { try { return new URL(u, ORIGIN).origin === ORIGIN; } catch { return false; } };

async function fetchText(u, redirect='follow') {
  const res = await fetch(u, { redirect });
  const text = await res.text().catch(()=> '');
  return { res, text };
}

async function readNetlifyTomlSummary() {
  try {
    const raw = await fs.readFile('netlify.toml', 'utf8');
    const redirects = (raw.match(/\[\[redirects\]\]/g) || []).length;
    console.log(`(info) netlify.toml present — redirect blocks: ${redirects}`);
  } catch {
    console.log(`(info) netlify.toml not found locally — skipping local summary (OK).`);
  }
}

async function getSitemap() {
  try {
    const { res, text } = await fetchText(`${ORIGIN}/sitemap.xml`, 'follow');
    if (res.ok && /<urlset/i.test(text)) {
      [...text.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)]
        .map(m => normalize(m[1]))
        .forEach(u => fromSitemap.add(u));
      console.log(`(info) sitemap URLs: ${fromSitemap.size}`);
    } else {
      console.log('(warn) sitemap.xml missing or unreadable');
    }
  } catch {
    console.log('(warn) failed to fetch sitemap.xml');
  }
}

function extractLinks($, base) {
  const out = [];
  $('a[href]').each((_, el) => {
    const href = ($(el).attr('href') || '').trim();
    if (!href || href.startsWith('mailto:') || href.startsWith('tel:')) return;
    try {
      const abs = new URL(href, base).toString();
      if (isInternal(abs)) out.push(normalize(abs));
    } catch {}
  });
  return out;
}

function issuesForCanonical(canon) {
  const issues = [];
  if (!canon) { issues.push('Missing canonical'); return issues; }
  let u;
  try { u = new URL(canon); } catch { issues.push('Canonical is not a valid absolute URL'); return issues; }
  if (u.protocol !== 'https:') issues.push('Canonical must be https');
  if (u.origin !== ORIGIN) issues.push(`Canonical origin must be ${ORIGIN}`);
  if (u.search) issues.push('Canonical must not include query');
  if (u.hash) issues.push('Canonical must not include fragment');
  const last = u.pathname.split('/').pop() || '';
  const looksLikeFile = last.includes('.');
  if (ENFORCE_TRAILING_SLASH && !looksLikeFile && !u.pathname.endsWith('/')) issues.push('Canonical should end with trailing slash');
  if (!ENFORCE_TRAILING_SLASH && u.pathname.endsWith('/') && u.pathname !== '/') issues.push('Canonical should NOT end with trailing slash');
  return issues;
}

async function auditPage(url) {
  const out = { url, issues: [] };
  const { res, text } = await fetchText(url, 'follow');
  if (!res.ok || !text) { out.issues.push(`Fetch failed: ${res.status}`); return out; }

  const $ = cheerio.load(text);
  const canonTags = $('link[rel="canonical"]');
  if (canonTags.length !== 1) out.issues.push(`Expected 1 canonical tag, found ${canonTags.length}`);
  const canonical = canonTags.first().attr('href') || '';
  const og = $('meta[property="og:url"]').attr('content') || '';
  if (!og) out.issues.push('Missing og:url');

  out.issues.push(...issuesForCanonical(canonical));
  if (og && canonical && !sameNorm(og, canonical)) {
    out.issues.push(`og:url does not match canonical\n  og:url: ${og}\n  canonical: ${canonical}`);
  }

  const expectedSelf = normalize(url);
  if (canonical && !sameNorm(canonical, expectedSelf)) {
    out.issues.push(`Canonical differs from expected self URL\n  expected: ${expectedSelf}\n  found:    ${canonical}`);
  }

  // Variant redirect checks (report-only)
  if (EXPECT_VARIANT_REDIRECTS) {
    const u = new URL(url);
    const path = u.pathname;

    // /no-slash -> /slash/
    const noSlash = path.endsWith('/') ? path.slice(0, -1) : path;
    if (noSlash && noSlash !== '') {
      const testNoSlash = `${ORIGIN}${noSlash}`;
      const r1 = await fetch(testNoSlash, { redirect: 'manual' });
      const loc1 = r1.headers.get('location');
      const ok301 = [301, 308].includes(r1.status) && loc1 && sameNorm(loc1, expectedSelf);
      if (!ok301) out.issues.push(`Per-page redirect failed (no-slash → slash)\n  GET ${testNoSlash}\n  status=${r1.status} location=${loc1 || '(none)'}`);
    }

    // .html -> /slash/
    const last = path.split('/').filter(Boolean).pop();
    const looksLikeFile = last && last.includes('.');
    if (last && !looksLikeFile) {
      const htmlVar = `${ORIGIN}${path.replace(/\/$/, '')}.html`;
      const r2 = await fetch(htmlVar, { redirect: 'manual' });
      const loc2 = r2.headers.get('location');
      const ok301b = [301, 308].includes(r2.status) && loc2 && sameNorm(loc2, expectedSelf);
      if (!ok301b) out.issues.push(`Per-page redirect failed (.html → slash)\n  GET ${htmlVar}\n  status=${r2.status} location=${loc2 || '(none)'}`);
    }
  }

  return out;
}

async function crawl() {
  while (toVisit.length && crawled.size < MAX_PAGES) {
    const { url, depth } = toVisit.shift();
    const key = normalize(url);
    if (visited.has(key)) continue;
    visited.add(key);
    crawled.add(key);

    await sleep(80);

    const { res, text } = await fetchText(url, 'follow');
    if (!res.ok || !text) continue;
    if (depth >= MAX_DEPTH) continue;

    const $ = cheerio.load(text);
    extractLinks($, url).forEach(next => { if (!visited.has(next)) toVisit.push({ url: next, depth: depth + 1 }); });
  }
}

(async () => {
  console.log('== REPORT-ONLY: affordable-handbags.com ==');
  await readNetlifyTomlSummary();
  await getSitemap();
  await crawl();

  const all = new Set([...fromSitemap, ...crawled]);
  const results = [];
  for (const u of all) results.push(await auditPage(u));

  let bad = 0;
  for (const r of results) {
    if (r.issues.length) {
      bad++;
      console.log(`\n❌ ${r.url}`);
      r.issues.forEach(i => console.log('  -', i));
    } else {
      console.log(`✅ ${r.url}`);
    }
  }

  // Coverage diff
  const missingInSitemap = [...crawled].filter(u => !fromSitemap.has(u));
  const orphanInSitemap  = [...fromSitemap].filter(u => !crawled.has(u));

  console.log('\n--- Coverage ---');
  console.log(`Crawled pages: ${crawled.size}`);
  console.log(`Sitemap URLs:  ${fromSitemap.size}`);

  if (missingInSitemap.length) {
    console.log('\nLIVE but NOT in sitemap (add these):');
    missingInSitemap.slice(0, 200).forEach(u => console.log('  -', u));
    if (missingInSitemap.length > 200) console.log(`  (+${missingInSitemap.length - 200} more)`);
  } else {
    console.log('\nAll crawled pages appear in the sitemap ✅');
  }

  if (orphanInSitemap.length) {
    console.log('\nIn sitemap but not reached by crawler (may be fine if unlinked):');
    orphanInSitemap.slice(0, 200).forEach(u => console.log('  -', u));
    if (orphanInSitemap.length > 200) console.log(`  (+${orphanInSitemap.length - 200} more)`);
  }

  if (bad) {
    console.log(`\nSummary: ${bad}/${results.length} pages with canonical/og or per-page redirect issues.`);
    process.exit(1);
  } else {
    console.log(`\nAll ${results.length} pages pass canonical + og:url + per-page redirect checks ✅`);
  }
})();

