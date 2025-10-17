import fs from "fs";
import path from "path";

const DRY = process.argv.includes("--dry");
const EMAIL = "affordable.handbags1@gmail.com";
const ORIGIN = "https://affordable-handbags.com";

const OUT = {
  rootDir: null,
  created: [],
  updated: [],
  notes: []
};

// 1) Find site root (where built HTML lives)
const CANDIDATE_DIRS = ["./", "./public", "./dist", "./build"];
function detectRoot() {
  for (const d of CANDIDATE_DIRS) {
    const p = path.resolve(d, "index.html");
    if (fs.existsSync(p)) {
      // Heuristic: assume this is the output root
      OUT.notes.push(`Detected root: ${path.resolve(d)}`);
      return path.resolve(d);
    }
  }
  return path.resolve("./"); // fallback
}
const ROOT = detectRoot();
OUT.rootDir = ROOT;

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }
function backupOnce(file) {
  if (!fs.existsSync(file)) return;
  const bak = file + ".bak";
  if (!fs.existsSync(bak)) fs.copyFileSync(file, bak);
}
function writeFile(p, content) {
  if (DRY) return;
  ensureDir(path.dirname(p));
  backupOnce(p);
  fs.writeFileSync(p, content, "utf8");
}

function read(file) { return fs.existsSync(file) ? fs.readFileSync(file, "utf8") : ""; }

// 2) Extract a shell (head..open body) + (close body..html) from index.html
function getShell() {
  const idx = path.join(ROOT, "index.html");
  const html = read(idx);
  // Minimal robust split
  const headOpen = html.match(/^[\s\S]*?<body[^>]*>/i);
  const tail = html.match(/<\/body>[\s\S]*$/i);
  const head = headOpen ? headOpen[0] : "<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Affordable Handbags</title></head><body>";
  const foot = tail ? tail[0] : "</body></html>";
  return { head, foot };
}
const SHELL = getShell();

// 3) Page builders (simple text, site-neutral)
function sectionWrap(inner) {
  return `\n<main class="container" style="max-width:900px;margin:2rem auto;padding:1rem;">\n${inner}\n</main>\n`;
}
function htmlDoc(inner) {
  // Insert inside <main> if present, else wrap
  let doc = SHELL.head;
  if (/<main[^>]*>/i.test(SHELL.head)) {
    doc = SHELL.head.replace(/<main[^>]*>/i, (m)=> m + "\n" + inner + "\n");
    return doc + SHELL.foot;
  }
  return SHELL.head + sectionWrap(inner) + SHELL.foot;
}

// English (default)
const EN = {
  about: htmlDoc(`
<h1>About Us</h1>
<p>Welcome to Affordable-Handbags.com! We publish simple guides, reviews, and recommendations to help you find stylish bags, backpacks, and wallets at budget-friendly prices.</p>
<p>This site is still developing — we'll add more articles and resources over time. Thanks for visiting!</p>
`),
  contact: htmlDoc(`
<h1>Contact Us</h1>
<p>Questions or suggestions? Reach us at:</p>
<p>📧 <a href="mailto:${EMAIL}">${EMAIL}</a></p>
<p>We usually respond within a few days.</p>
`),
  terms: htmlDoc(`
<h1>Terms &amp; Conditions</h1>
<p>By using this site, you agree to these terms. Content is informational and may include affiliate links. We do not guarantee availability, pricing, or inventory from third-party stores.</p>
<p>Please do not reproduce content without permission. For legal questions, contact us by email.</p>
`)
};

// Spanish
const ES = {
  about: htmlDoc(`
<h1>Sobre Nosotros</h1>
<p>¡Bienvenidos a Affordable-Handbags.com! Publicamos guías sencillas, reseñas y recomendaciones para ayudarte a encontrar bolsos, mochilas y carteras con estilo a precios accesibles.</p>
<p>Este sitio está en desarrollo; iremos sumando artículos y recursos con el tiempo. ¡Gracias por visitarnos!</p>
`),
  contact: htmlDoc(`
<h1>Contacto</h1>
<p>¿Preguntas o sugerencias? Escríbenos:</p>
<p>📧 <a href="mailto:${EMAIL}">${EMAIL}</a></p>
<p>Normalmente respondemos en unos días.</p>
`),
  terms: htmlDoc(`
<h1>Términos y Condiciones</h1>
<p>Al usar este sitio, aceptas estos términos. El contenido es informativo y puede incluir enlaces de afiliado. No garantizamos disponibilidad, precios ni inventarios de tiendas de terceros.</p>
<p>No reproduzcas contenido sin permiso. Para consultas legales, contáctanos por correo.</p>
`)
};

// 4) Target paths (English default has no /en/)
const PAGES = [
  { file: path.join(ROOT, "about", "index.html"), html: EN.about, url: "/about/" },
  { file: path.join(ROOT, "contact", "index.html"), html: EN.contact, url: "/contact/" },
  { file: path.join(ROOT, "terms", "index.html"), html: EN.terms, url: "/terms/" },

  { file: path.join(ROOT, "es", "sobre-nosotros", "index.html"), html: ES.about, url: "/es/sobre-nosotros/" },
  { file: path.join(ROOT, "es", "contacto", "index.html"), html: ES.contact, url: "/es/contacto/" },
  { file: path.join(ROOT, "es", "terminos", "index.html"), html: ES.terms, url: "/es/terminos/" }
];

// 5) Write pages
for (const p of PAGES) {
  if (!DRY) writeFile(p.file, p.html);
  OUT.created.push(p.file);
}

// 6) Update sitemap.xml (create if missing). Add/merge unique loc entries.
function updateSitemap() {
  const smPath = path.join(ROOT, "sitemap.xml");
  const now = new Date().toISOString();
  const urls = PAGES.map(p => p.url);
  let xml = read(smPath).trim();
  const urlsetOpen = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`;
  const urlsetClose = `</urlset>\n`;
  if (!xml) {
    xml = urlsetOpen + "\n" + urls.map(u => `  <url><loc>${ORIGIN}${u}</loc><lastmod>${now}</lastmod></url>`).join("\n") + "\n" + urlsetClose;
  } else {
    // Insert any missing urls
    for (const u of urls) {
      const re = new RegExp(`<loc>\\s*${ORIGIN.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')}${u.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')}\\s*</loc>`, "i");
      if (!re.test(xml)) {
        // Insert before closing tag
        const block = `  <url><loc>${ORIGIN}${u}</loc><lastmod>${now}</lastmod></url>\n`;
        xml = xml.replace(/<\/urlset>\s*$/i, block + "</urlset>\n");
      }
    }
  }
  if (!DRY) { backupOnce(smPath); fs.writeFileSync(smPath, xml, "utf8"); }
  OUT.updated.push(smPath);
}
updateSitemap();

// 7) Append redirects to netlify.toml (html → slash). Keep existing content.
function updateNetlifyToml() {
  const nf = path.resolve("netlify.toml");
  const existing = read(nf);
  let toml = existing || "";
  const have = (from, to) => new RegExp(`\\[\\[redirects\\]\\][\\s\\S]*?from\\s*=\\s*"?${from.replace(/\//g,"\\/")}"?[\\s\\S]*?to\\s*=\\s*"?${to.replace(/\//g,"\\/")}"?`, "i").test(toml);

  const pairs = [
    ["/about.html", "/about/"],
    ["/contact.html", "/contact/"],
    ["/terms.html", "/terms/"],
    ["/es/sobre-nosotros.html", "/es/sobre-nosotros/"],
    ["/es/contacto.html", "/es/contacto/"],
    ["/es/terminos.html", "/es/terminos/"]
  ];

  let added = 0;
  for (const [from, to] of pairs) {
    if (!have(from, to)) {
      toml += `

[[redirects]]
from = "${from}"
to = "${to}"
status = 301
force = true
`;
      added++;
    }
  }
  if (added > 0 && !DRY) { backupOnce(nf); fs.writeFileSync(nf, toml, "utf8"); }
  if (added > 0) OUT.updated.push(nf);
}
updateNetlifyToml();

// 8) Print summary
console.log("===== BASIC PAGES REPORT =====");
console.log(`Mode: ${DRY ? "DRY-RUN (no writes)" : "APPLY (files written)"}`);
console.log(`Root: ${ROOT}`);
console.log(`Pages created: ${OUT.created.length}`);
for (const f of OUT.created) console.log(" + " + path.relative(process.cwd(), f));
console.log(`Files updated: ${OUT.updated.length}`);
for (const f of OUT.updated) console.log(" * " + path.relative(process.cwd(), f));
for (const n of OUT.notes) console.log(" - " + n);

