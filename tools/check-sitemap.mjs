const ORIGIN = 'https://affordable-handbags.com';

function norm(u) {
  const x = new URL(u);
  x.hash = ''; x.search = '';
  const last = x.pathname.split('/').filter(Boolean).pop() || '';
  const looksFile = last.includes('.');
  if (!looksFile && !x.pathname.endsWith('/')) x.pathname += '/';
  return x.toString();
}

async function fetchText(u){
  const r = await fetch(u);
  return r.ok ? r.text() : '';
}

(async () => {
  const xml = await fetchText(`${ORIGIN}/sitemap.xml`);
  if (!xml || !xml.includes('<urlset')) {
    console.log('❌ sitemap.xml missing or unreadable');
    process.exit(1);
  }

  const locs = [...xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map(m => m[1]);
  const issues = [];
  const seen = new Set();

  for (const u of locs) {
    let parsed;
    try { parsed = new URL(u); } catch { issues.push(`Invalid URL: ${u}`); continue; }
    if (parsed.protocol !== 'https:') issues.push(`Not HTTPS: ${u}`);
    if (parsed.search) issues.push(`Has querystring: ${u}`);
    if (parsed.hash) issues.push(`Has fragment: ${u}`);
    if (parsed.pathname.endsWith('.html')) issues.push(`Points to .html: ${u}`);

    const last = parsed.pathname.split('/').filter(Boolean).pop() || '';
    const looksFile = last.includes('.');
    if (!looksFile && !parsed.pathname.endsWith('/')) issues.push(`Missing trailing slash: ${u}`);

    const n = norm(u);
    if (seen.has(n)) issues.push(`Duplicate (normalized): ${u}`);
    seen.add(n);
  }

  if (issues.length) {
    console.log('❌ Sitemap issues found:');
    issues.slice(0, 300).forEach(i => console.log(' -', i));
    process.exit(1);
  } else {
    console.log(`✅ Sitemap looks good (${locs.length} URLs)`);
  }
})();

