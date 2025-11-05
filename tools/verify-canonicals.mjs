import * as cheerio from "cheerio";

const ORIGIN = "https://affordable-handbags.com";
const ENFORCE_TRAILING_SLASH = true;
const MAX_PAGES = 200; // adjust if needed
const MAX_DEPTH = 2;

const visited = new Set();
const queue = [`${ORIGIN}/`];
const results = [];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function normalize(url) {
  const u = new URL(url, ORIGIN);
  u.hash = "";
  u.search = "";
  const last = u.pathname.split("/").filter(Boolean).pop() || "";
  const looksFile = last.includes(".");
  if (ENFORCE_TRAILING_SLASH && !looksFile && !u.pathname.endsWith("/")) u.pathname += "/";
  return u.toString();
}

const sameNorm = (a, b) => normalize(a) === normalize(b);

async function fetchHtml(u) {
  try {
    const res = await fetch(u, { redirect: "follow" });
    if (!res.ok) return null;
    return await res.text();
  } catch {
    return null;
  }
}

function extractLinks($, base) {
  const out = [];
  $("a[href]").each((_, el) => {
    const href = ($(el).attr("href") || "").trim();
    if (!href || href.startsWith("#") || href.startsWith("mailto:") || href.startsWith("tel:")) return;
    try {
      const abs = new URL(href, base).toString();
      if (abs.startsWith(ORIGIN)) out.push(normalize(abs));
    } catch {}
  });
  return out;
}

async function auditPage(url) {
  const html = await fetchHtml(url);
  if (!html) return { url, ok: false, reason: "Fetch failed" };

  const $ = cheerio.load(html);
  const canon = $('link[rel="canonical"]').attr("href") || "";
  const og = $('meta[property="og:url"]').attr("content") || "";
  const expected = normalize(url);
  const issues = [];

  if (!canon) issues.push("Missing canonical");
  if (!og) issues.push("Missing og:url");

  if (canon && !sameNorm(canon, expected)) issues.push(`Canonical mismatch → ${canon}`);
  if (og && !sameNorm(og, expected)) issues.push(`og:url mismatch → ${og}`);

  const uniqueCanon = $('link[rel="canonical"]').length;
  if (uniqueCanon > 1) issues.push(`Multiple canonical tags (${uniqueCanon})`);

  return { url, ok: issues.length === 0, issues };
}

async function crawl() {
  while (queue.length && visited.size < MAX_PAGES) {
    const url = queue.shift();
    if (visited.has(url)) continue;
    visited.add(url);

    const html = await fetchHtml(url);
    if (!html) continue;

    const $ = cheerio.load(html);
    const pageLinks = extractLinks($, url);
    for (const link of pageLinks) if (!visited.has(link)) queue.push(link);
    const result = await auditPage(url);
    results.push(result);
    await sleep(100);
  }
}

(async () => {
  console.log("🔎 Verifying canonical + og:url consistency across site…\n");
  
  await crawl();
  
  const good = results.filter((r) => r.ok);
  const bad = results.filter((r) => !r.ok);
  
  console.log(`\n✅ PASSED: ${good.length} pages`);
  console.log(`❌ FAILED: ${bad.length} pages\n`);
  
  if (bad.length > 0) {
    console.log("Issues found:\n");
    bad.forEach((r) => {
      console.log(`❌ ${r.url}`);
      if (r.reason) console.log(`   → ${r.reason}`);
      r.issues?.forEach((issue) => console.log(`   → ${issue}`));
      console.log("");
    });
  }
  
  console.log(`\nCrawled ${visited.size} unique URLs`);
  
  process.exit(bad.length > 0 ? 1 : 0);
})();

