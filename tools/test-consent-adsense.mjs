import * as cheerio from "cheerio";
import fs from "fs/promises";
import puppeteer from "puppeteer";

const SITE = process.env.SITE || "https://affordable-handbags.com";
const GTM_ID = process.env.GTM_ID || "GTM-TCG7SMDD";
const EXPECTED_ADSTXT = process.env.EXPECTED_ADSTXT || "google.com, pub-8379967738924229, DIRECT, f08c47fec0942fa0";

// Simple helpers
const sleep = (ms)=> new Promise(r=>setTimeout(r, ms));
function absolute(u){ return new URL(u, SITE).toString(); }
function isInternal(u){ try { return new URL(u).origin === new URL(SITE).origin; } catch { return false; } }

// Popular CMP script signatures
const CMP_SIGNATURES = [
  /fundingchoicesmessages\.google\.com\/.*fc\.js/i,  // Google Funding Choices
  /otSDKStub\.js/i,                                  // OneTrust
  /cookieconsent(?:\.min)?\.js/i,                    // CookieYes / Osano patterns
  /consent\.cookiebot\.com/i,                        // Cookiebot
  /quantcast\.mp\.quantserve\.com/i,                 // Quantcast Choice
  /cdn\.privacy-mgmt\.com/i,                         // Didomi / Sourcepoint
  /iubenda\.com\/consent/i                           // Iubenda
];

// AdSense / ads network URLs to watch
const ADSENSE_URLS = [
  /pagead2\.googlesyndication\.com\/pagead\/js\/adsbygoogle\.js/i,
  /googleads\.g\.doubleclick\.net/i,
  /securepubads\.g\.doubleclick\.net/i,
  /tpc\.googlesyndication\.com/i
];

// GA/gtag/analytics files to watch (for premature load)
const GA_URLS = [
  /www\.googletagmanager\.com\/gtag\/js/i,
  /www\.google-analytics\.com\/g\/collect/i
];

// Pages to sample
const START_PAGES = [`${SITE}/`];

async function fetchText(u){
  try {
    const r = await fetch(u);
    return r.ok ? await r.text() : "";
  } catch { return ""; }
}

function findScriptsOrder($){
  const order = [];
  $("script[src]").each((_,el)=>{
    const src = ($(el).attr("src")||"").trim();
    if (!src) return;
    order.push(src);
  });
  return order;
}

function detectCMP($){
  const order = findScriptsOrder($);
  const hits = order.filter(src => CMP_SIGNATURES.some(rx => rx.test(src)));
  return { hasCMP: hits.length>0, matches: hits };
}

function detectGTM($, gtmId){
  const order = findScriptsOrder($);
  // Check both external script src AND inline script content for GTM
  let hasGTM = order.some(src => new RegExp(`googletagmanager\\.com\\/gtm\\.js\\?id=${gtmId}`, "i").test(src));
  
  // Also check inline scripts for GTM code
  if (!hasGTM) {
    $("script").each((_, el) => {
      const content = $(el).html() || "";
      if (content.includes("googletagmanager.com/gtm.js") && content.includes(gtmId)) {
        hasGTM = true;
      }
    });
  }
  
  // Also check noscript iframe somewhere in body (not mandatory to be in head)
  const hasNoscript = $("noscript iframe[src*='googletagmanager.com/ns.html?id=']").length > 0;
  return { hasGTM, hasNoscript, order };
}

function scanConsentAPIs(html){
  const issues = [];
  const hasDefault = /gtag\(['"]consent['"]\s*,\s*['"]default['"]\s*,/i.test(html);
  const hasUpdate  = /gtag\(['"]consent['"]\s*,\s*['"]update['"]\s*,/i.test(html);

  // Scan for the signals we hope to see managed by CMP defaults
  const keys = ["ad_storage","analytics_storage","ad_user_data","ad_personalization"];
  const foundKeys = {};
  for (const k of keys){
    const rx = new RegExp(`['"]${k}['"]\\s*:\\s*['"](granted|denied)['"]`, "i");
    foundKeys[k] = rx.test(html);
  }

  // Optional region scoping (good practice)
  const regionScoped = /region\s*:\s*\[[^\]]+\]/i.test(html);

  return { hasDefault, hasUpdate, foundKeys, regionScoped, issues };
}

function cmpBeforeGtm(order, cmpMatches, gtmId){
  if (!cmpMatches.length) return null;
  const cmpIndex = order.findIndex(src => cmpMatches.includes(src));
  const gtmIndex = order.findIndex(src => new RegExp(`googletagmanager\\.com\\/gtm\\.js\\?id=${gtmId}`,'i').test(src));
  if (cmpIndex === -1 || gtmIndex === -1) return null;
  return cmpIndex < gtmIndex;
}

async function testAdsTxt(site, expectedLine){
  const u = new URL("/ads.txt", site).toString();
  const txt = await fetchText(u);
  const lines = txt.split(/\r?\n/).map(s=>s.trim()).filter(Boolean);
  const ok = lines.some(l => l.toLowerCase() === expectedLine.toLowerCase());
  return { ok, url: u, foundLine: ok ? expectedLine : (lines[0] || "(none)"), allLines: lines };
}

async function collectInternalLinks(html, base, max=5){
  const $ = cheerio.load(html);
  const links = new Set();
  $("a[href]").each((_,el)=>{
    const href = ($(el).attr("href")||"").trim();
    if (!href || href.startsWith("#") || href.startsWith("mailto:") || href.startsWith("tel:")) return;
    try {
      const abs = new URL(href, base).toString();
      if (isInternal(abs)) links.add(abs);
    } catch {}
  });
  return [...links].slice(0, max);
}

async function staticAudit(url){
  const html = await fetchText(url);
  if (!html) return { url, error: "Fetch failed" };
  const $ = cheerio.load(html);

  const cmp = detectCMP($);
  const gtm = detectGTM($, GTM_ID);
  const consent = scanConsentAPIs(html);

  const order = gtm.order;
  const cmpFirst = cmpBeforeGtm(order, cmp.matches, GTM_ID);

  const notes = [];
  if (!cmp.hasCMP) notes.push("CMP script not detected in <head>.");
  if (!gtm.hasGTM) notes.push(`GTM container ${GTM_ID} not found.`);
  if (!consent.hasDefault) notes.push("Missing gtag('consent','default', …) call.");
  if (!consent.foundKeys.ad_storage) notes.push("No explicit ad_storage default found.");
  if (!consent.foundKeys.analytics_storage) notes.push("No explicit analytics_storage default found.");
  if (cmp.hasCMP && gtm.hasGTM && cmpFirst === false) notes.push("CMP script appears AFTER GTM — move CMP before GTM.");

  return { url, cmp, gtm, consent, cmpFirst, notes };
}

async function runtimeAudit(url){
  const browser = await puppeteer.launch({headless:"new", args:["--no-sandbox","--disable-setuid-sandbox"]});
  const page = await browser.newPage();

  // Emulate EEA-ish locale (not IP-based, but helps many CMPs show banners)
  await page.emulateTimezone("Europe/Berlin");
  await page.setExtraHTTPHeaders({ "Accept-Language": "de,en;q=0.9" });

  const seen = { ads:false, adsHits:[], ga:false, gaHits:[], console:[] };

  page.on("console", msg => seen.console.push(msg.text()));
  page.on("request", req => {
    const url = req.url();
    if (ADSENSE_URLS.some(rx => rx.test(url))) seen.adsHits.push(url);
    if (GA_URLS.some(rx => rx.test(url))) seen.gaHits.push(url);
  });

  await page.goto(url, { waitUntil:"domcontentloaded", timeout: 60000 });
  // Wait a bit for any auto-loading scripts (without interacting with CMP)
  await sleep(8000);

  await browser.close();
  seen.ads = seen.adsHits.length>0;
  seen.ga  = seen.gaHits.length>0;
  return { url, seen };
}

(async () => {
  const report = { site:SITE, timestamp:new Date().toISOString(), pages:[] };

  // 1) ads.txt
  const ads = await testAdsTxt(SITE, EXPECTED_ADSTXT);
  report.adsTxt = ads;

  // 2) Pick pages to test
  const homeHtml = await fetchText(`${SITE}/`);
  const internals = homeHtml ? await collectInternalLinks(homeHtml, `${SITE}/`, 4) : [];
  const targets = [ `${SITE}/`, ...internals ];

  // 3) Static + Runtime for each target
  for (const u of targets){
    const s = await staticAudit(u);
    let r = { url:u, runtimeError:"(skipped)" };
    try { r = await runtimeAudit(u); } catch(e){ r = { url:u, runtimeError:e.message || "runtime failed" }; }
    report.pages.push({ static:s, runtime:r });
  }

  // 4) Print human summary
  console.log(`\n== Consent Mode / AdSense Audit for ${SITE} ==`);
  console.log(`ads.txt @ ${ads.url}: ${ads.ok ? "✅ OK" : "❌ Missing/invalid"}`);
  if (!ads.ok){
    console.log(`  Expected: ${EXPECTED_ADSTXT}`);
    console.log(`  First line found: ${ads.foundLine}`);
  }

  let anyIssues = !ads.ok;
  for (const p of report.pages){
    const s = p.static, r = p.runtime;
    console.log(`\n— ${s.url}`);
    if (s.error){ console.log(`  ❌ Fetch failed`); anyIssues = true; continue; }

    // Static checks
    console.log(`  CMP detected: ${s.cmp.hasCMP ? "✅" : "❌"} ${s.cmp.matches.join(", ") || ""}`);
    console.log(`  GTM ${GTM_ID} present: ${s.gtm.hasGTM ? "✅" : "❌"}`);
    console.log(`  Consent API: default=${s.consent.hasDefault ? "✅" : "❌"} update=${s.consent.hasUpdate ? "✅" : "❌"}`);
    console.log(`  Keys: ad_storage=${s.consent.foundKeys.ad_storage?"✅":"❌"}, analytics_storage=${s.consent.foundKeys.analytics_storage?"✅":"❌"}, ad_user_data=${s.consent.foundKeys.ad_user_data?"✅":"⚠️ missing"}, ad_personalization=${s.consent.foundKeys.ad_personalization?"✅":"⚠️ missing"}`);
    if (s.cmpFirst === false) { console.log(`  ❌ CMP loads AFTER GTM (move CMP above GTM)`); anyIssues = true; }
    if (s.notes.length){ s.notes.forEach(n=>{ console.log("  ❌ " + n); anyIssues = true; }); }

    // Runtime checks (no banner interaction)
    if (r.runtimeError){
      console.log(`  ⚠️ Runtime check skipped/failed: ${r.runtimeError}`);
    } else {
      const adsEarly = r.seen.adsHits.length ? "❌ loaded BEFORE consent (likely)" : "✅ not loaded pre-consent";
      const gaEarly  = r.seen.gaHits.length  ? "⚠️ GA loaded pre-consent" : "✅ GA not loaded pre-consent";
      console.log(`  Network (first ~8s, no clicks):`);
      console.log(`    AdSense: ${adsEarly}`);
      if (r.seen.adsHits.length) r.seen.adsHits.slice(0,3).forEach(h=>console.log(`      ↳ ${h}`));
      console.log(`    GA4: ${gaEarly}`);
      if (r.seen.gaHits.length) r.seen.gaHits.slice(0,3).forEach(h=>console.log(`      ↳ ${h}`));
      if (r.seen.adsHits.length) anyIssues = true;
    }
  }

  console.log("\n== Verdict ==");
  if (anyIssues){
    console.log("❌ Issues detected. See lines above for fixes (CMP before GTM; add consent defaults; block ads until consent; verify ads.txt).");
    process.exit(1);
  } else {
    console.log("✅ Looks good: CMP present, Consent API found, and no AdSense requests before consent.");
  }
})();

