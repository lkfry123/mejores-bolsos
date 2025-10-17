import fs from "fs";
import path from "path";

const DRY = process.argv.includes("--dry");
const ENFORCED_GTM = "GTM-TCG7SMDD";
const OLD_GTM = "GT-MR24WCXH";                 // also catch GTM-MR24WCXH
const GA4_ID = "G-H1Q1KL01RP";

const exts = new Set([".html",".htm",".ejs",".njk",".liquid",".vue",".svelte",".astro",".php",".erb",".jsp",".js",".jsx",".ts",".tsx"]);
const projectRoot = process.cwd();

const summary = {
  scanned: 0,
  changed: 0,
  removedOldGtm: [],
  removedGa4Standalone: [],
  insertedHead: [],
  insertedNoscript: [],
  replacedWrongGtmId: [],
  skippedNoHeadOrBody: []
};

function* walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".git")) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walk(full);
    } else {
      const ext = path.extname(entry.name).toLowerCase();
      if (exts.has(ext)) yield full;
    }
  }
}

function backupFile(file) {
  const bak = file + ".bak";
  if (!fs.existsSync(bak)) fs.copyFileSync(file, bak);
}

function removeScriptTagContaining(urlRe, content) {
  // remove <script ... src="...urlRe..."></script>
  const re = new RegExp(`<script[^>]*?src=["'][^"']*${urlRe.source}[^"']*["'][\\s\\S]*?<\\/script>\\s*`, "gi");
  return content.replace(re, "");
}

function removeNoscriptIframeContaining(urlRe, content) {
  // remove <noscript><iframe src="...urlRe..."></iframe></noscript>
  const re = new RegExp(`<noscript>[\\s\\S]*?src=["'][^"']*${urlRe.source}[^"']*["'][\\s\\S]*?<\\/noscript>\\s*`, "gi");
  return content.replace(re, "");
}

function removeInlineInitForGA4(id, content) {
  // remove <script> ... gtag('config','G-...') ... </script>
  const re = new RegExp(`<script\\b[^>]*>[\\s\\S]*?gtag\\(\\s*['"]config['"]\\s*,\\s*['"]${id}['"][\\s\\S]*?\\)\\s*;?[\\s\\S]*?<\\/script>\\s*`, "gi");
  return content.replace(re, "");
}

function ensureHeadSnippet(content) {
  const headOpen = content.match(/<head[^>]*>/i);
  if (!headOpen) return { content, inserted: false, noHead: true };
  const already = new RegExp(`gtm\\.js\\?id=${ENFORCED_GTM}`, "i").test(content);
  if (already) return { content, inserted: false, noHead: false };

  const snippet =
`<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','${ENFORCED_GTM}');</script>
<!-- End Google Tag Manager -->
`;

  const idx = headOpen.index + headOpen[0].length;
  const newContent = content.slice(0, idx) + "\n" + snippet + content.slice(idx);
  return { content: newContent, inserted: true, noHead: false };
}

function ensureNoscriptSnippet(content) {
  const bodyOpen = content.match(/<body[^>]*>/i);
  if (!bodyOpen) return { content, inserted: false, noBody: true };
  const already = new RegExp(`ns\\.html\\?id=${ENFORCED_GTM}`, "i").test(content);
  if (already) return { content, inserted: false, noBody: false };

  const snippet =
`<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=${ENFORCED_GTM}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
`;

  const idx = bodyOpen.index + bodyOpen[0].length;
  const newContent = content.slice(0, idx) + "\n" + snippet + content.slice(idx);
  return { content: newContent, inserted: true, noBody: false };
}

function replaceWrongGtmIds(content) {
  // If there is a GTM/GT- container other than ENFORCED_GTM, switch it to ENFORCED_GTM
  const reId = /((?:GTM|GT)-[A-Z0-9_-]+)/ig;
  let changed = false;
  const newContent = content.replace(reId, (m) => {
    if (/^GTM-?TCG7SMDD$/i.test(m)) return m;      // already correct
    if (/^GT-?MR24WCXH$/i.test(m)) { changed = true; return ENFORCED_GTM; }
    // For other container IDs, leave them unless they are used in gtm.js/ns.html includes
    return m;
  });

  // In loader URLs, force to ENFORCED_GTM if not already
  const reLoader = /((?:gtm|ns)\.html\?id=|gtm\.js\?id=)(GTM|GT)-[A-Z0-9_-]+/ig;
  const newer = newContent.replace(reLoader, (_m, prefix) => {
    changed = true;
    return `${prefix}${ENFORCED_GTM}`;
  });

  return { content: newer, changed };
}

function processFile(file) {
  let content = fs.readFileSync(file, "utf8");
  const original = content;
  let changed = false;

  // 1) Remove old GTM (GT/ GTM - MR24WCXH)
  const urlReOldLoader = /www\.googletagmanager\.com\/gtm\.js\?id=(?:GTM|GT)-MR24WCXH/i;
  const urlReOldNS = /www\.googletagmanager\.com\/ns\.html\?id=(?:GTM|GT)-MR24WCXH/i;

  let before = content;
  content = removeScriptTagContaining(urlReOldLoader, content);
  content = removeNoscriptIframeContaining(urlReOldNS, content);
  if (content !== before) {
    changed = true;
    summary.removedOldGtm.push(file);
  }

  // 2) Remove stand-alone GA4 loader + inline init for our GA4_ID
  const urlReGaLoader = new RegExp(`www\\.googletagmanager\\.com\\/gtag\\/js\\?id=${GA4_ID.replace("-", "\\-")}`, "i");
  before = content;
  content = removeScriptTagContaining(urlReGaLoader, content);
  content = removeInlineInitForGA4(GA4_ID, content);
  if (content !== before) {
    changed = true;
    summary.removedGa4Standalone.push(file);
  }

  // 3) Ensure correct GTM head + noscript
  // Only for "full" docs that have <head> / <body>
  const hasHead = /<head[^>]*>/i.test(content);
  const hasBody = /<body[^>]*>/i.test(content);

  if (hasHead) {
    const r1 = ensureHeadSnippet(content);
    if (r1.inserted) { changed = true; summary.insertedHead.push(file); }
    content = r1.content;
  } else {
    summary.skippedNoHeadOrBody.push(file);
  }

  if (hasBody) {
    const r2 = ensureNoscriptSnippet(content);
    if (r2.inserted) { changed = true; summary.insertedNoscript.push(file); }
    content = r2.content;
  } else {
    if (!summary.skippedNoHeadOrBody.includes(file)) summary.skippedNoHeadOrBody.push(file);
  }

  // 4) Replace wrong GTM IDs in loader URLs (surgical)
  const r3 = replaceWrongGtmIds(content);
  if (r3.changed) { changed = true; summary.replacedWrongGtmId.push(file); }
  content = r3.content;

  if (changed && !DRY) {
    backupFile(file);
    fs.writeFileSync(file, content, "utf8");
  }

  if (changed) summary.changed += 1;
}

for (const file of walk(projectRoot)) {
  summary.scanned += 1;
  try { processFile(file); } catch (e) { /* ignore but continue */ }
}

// Print summary
const out = [];
out.push("===== TAG FIX REPORT =====");
out.push(`Mode: ${DRY ? "DRY-RUN (no writes)" : "APPLY (files updated)"}`);
out.push(`Files scanned: ${summary.scanned}`);
out.push(`Files changed: ${summary.changed}`);
out.push(`Removed old GTM (${OLD_GTM}): ${summary.removedOldGtm.length}`);
out.push(`Removed stand-alone GA4 (${GA4_ID}): ${summary.removedGa4Standalone.length}`);
out.push(`Inserted GTM head (${ENFORCED_GTM}): ${summary.insertedHead.length}`);
out.push(`Inserted GTM noscript (${ENFORCED_GTM}): ${summary.insertedNoscript.length}`);
out.push(`Replaced wrong GTM IDs in URLs: ${summary.replacedWrongGtmId.length}`);
out.push(`Skipped (no <head>/<body>): ${summary.skippedNoHeadOrBody.length}`);
if (summary.removedOldGtm.length) out.push("\nOld GTM removed from:\n - " + summary.removedOldGtm.join("\n - "));
if (summary.removedGa4Standalone.length) out.push("\nStandalone GA4 removed from:\n - " + summary.removedGa4Standalone.join("\n - "));
if (summary.insertedHead.length) out.push("\nHead snippet inserted in:\n - " + summary.insertedHead.join("\n - "));
if (summary.insertedNoscript.length) out.push("\nNoscript snippet inserted in:\n - " + summary.insertedNoscript.join("\n - "));
if (summary.replacedWrongGtmId.length) out.push("\nLoader IDs replaced in:\n - " + summary.replacedWrongGtmId.join("\n - "));
if (summary.skippedNoHeadOrBody.length) out.push("\nSkipped (partials):\n - " + summary.skippedNoHeadOrBody.join("\n - "));
console.log(out.join("\n"));

