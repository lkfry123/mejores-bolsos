const ORIGIN = 'https://affordable-handbags.com';
const MAX_SUGGEST = 100;

function norm(u) {
  const x = new URL(u, ORIGIN);
  x.hash = ''; x.search = '';
  // enforce slash for non-file
  const last = x.pathname.split('/').filter(Boolean).pop() || '';
  const looksFile = last.includes('.');
  if (!looksFile && !x.pathname.endsWith('/')) x.pathname += '/';
  return x.toString();
}

async function fetchText(u, redirect='follow') {
  const res = await fetch(u, { redirect });
  const text = await res.text().catch(()=> '');
  return { res, text };
}

async function getSitemapUrls() {
  const out = new Set();
  try {
    const { res, text } = await fetchText(`${ORIGIN}/sitemap.xml`);
    if (res.ok && /<urlset/i.test(text)) {
      [...text.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)]
        .map(m => norm(m[1]))
        .forEach(u => out.add(u));
    }
  } catch {}
  if (!out.size) out.add(`${ORIGIN}/`);
  return [...out];
}

function priorityScore(u) {
  // Simple heuristic: fewer path segments = higher priority
  const p = new URL(u).pathname.split('/').filter(Boolean);
  return p.length;
}

(async () => {
  const urls = await getSitemapUrls();
  // prioritize shorter paths first
  urls.sort((a,b) => priorityScore(a) - priorityScore(b));

  const miss = [];
  for (const u of urls) {
    if (miss.length >= MAX_SUGGEST) break;

    const U = new URL(u);
    const path = U.pathname;
    const expected = norm(u);

    // /no-slash -> /slash/
    if (path !== '/') {
      const noSlash = `${ORIGIN}${path.endsWith('/') ? path.slice(0,-1) : path}`;
      const r1 = await fetch(noSlash, { redirect: 'manual' });
      const loc1 = r1.headers.get('location');
      const ok1 = [301,308].includes(r1.status) && loc1 && norm(loc1) === expected;
      if (!ok1) miss.push({ from: new URL(noSlash).pathname, to: new URL(expected).pathname });
    }

    // .html -> /slash/
    const last = path.split('/').filter(Boolean).pop();
    const looksFile = last && last.includes('.');
    if (!looksFile && path !== '/') {
      const htmlVar = `${ORIGIN}${path.replace(/\/$/, '')}.html`;
      const r2 = await fetch(htmlVar, { redirect: 'manual' });
      const loc2 = r2.headers.get('location');
      const ok2 = [301,308].includes(r2.status) && loc2 && norm(loc2) === expected;
      if (!ok2) miss.push({ from: new URL(htmlVar).pathname, to: new URL(expected).pathname });
    }
  }

  // De-duplicate
  const seen = new Set();
  const uniq = miss.filter(r => {
    const k = r.from + '→' + r.to;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  }).slice(0, MAX_SUGGEST);

  if (!uniq.length) {
    console.log('All checked sitemap URLs have working variant redirects ✅');
    return;
  }

  console.log('\n# Paste ONLY what you need into netlify.toml (per-page). Keep it small.\n');
  for (const r of uniq) {
    console.log('[[redirects]]');
    console.log(`  from = "${r.from}"`);
    console.log(`  to = "${r.to}"`);
    console.log('  status = 301\n');
  }
})();

