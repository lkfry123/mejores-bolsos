import { writeFile, readFile } from 'fs/promises';

const ORIGIN = 'https://affordable-handbags.com';
const TARGET = `${ORIGIN}/`;

function findAll(re, s) { const out=[]; let m; while ((m=re.exec(s))) out.push({i:m.index, m}); return out; }
function idx(s, sub){ const i=s.indexOf(sub); return i<0?null:i; }

function hasKeys(jsonTxt, keys){
  try{ const o = Function('"use strict";return ('+jsonTxt+')')(); 
    return keys.every(k => Object.prototype.hasOwnProperty.call(o, k));
  }catch{ return false; }
}

(async()=>{
  const res = await fetch(TARGET, { redirect: 'follow' });
  const html = await res.text();
  const report = [];

  // 1) CMP hints (static scan)
  const tcfapiRefs = findAll(/__tcfapi|tcfapi|iabeurope|consentmanager|oneTrust|quantcast|didomi|fundingchoices/ig, html);
  report.push(`CMP hints found: ${tcfapiRefs.length} (${tcfapiRefs.slice(0,5).map(x=>x.m[0]).join(', ') || 'none'})`);

  // 2) GTM present?
  const gtmScript = idx(html, 'googletagmanager.com/gtm.js?id=');
  report.push(`GTM snippet present: ${gtmScript !== null ? 'YES' : 'NO'}`);

  // 3) Consent Mode default/update calls in HTML?
  //    Look for gtag('consent','default'...'analytics_storage'...)
  const defaultCalls = findAll(/gtag\(\s*['"]consent['"]\s*,\s*['"]default['"]\s*,\s*(\{[\s\S]*?\})\s*\)/g, html);
  const updateCalls  = findAll(/gtag\(\s*['"]consent['"]\s*,\s*['"]update['"]\s*,\s*(\{[\s\S]*?\})\s*\)/g, html);

  const REQUIRED = ['ad_user_data','ad_personalization','ad_storage','analytics_storage'];
  let defaultOk = false;
  for (const call of defaultCalls) {
    const ok = hasKeys(call.m[1], REQUIRED);
    if (ok) { defaultOk = true; break; }
  }
  report.push(`Consent Mode DEFAULT present: ${defaultCalls.length>0 ? 'YES' : 'NO'}`);
  report.push(`DEFAULT includes CMv2 keys (${REQUIRED.join(', ')}): ${defaultOk ? 'YES' : 'NO'}`);
  report.push(`Consent Mode UPDATE present: ${updateCalls.length>0 ? 'YES' : 'NO'}`);

  // 4) Heuristic: CMP before GTM?
  const cmpIdx = Math.min(
    ...[ '__tcfapi', 'tcfapi', 'FundingChoices', 'OneTrust', 'Didomi', 'Quantcast' ]
      .map(k => idx(html, k))
      .filter(v => v !== null)
  );
  const orderMsg = (cmpIdx !== Infinity && cmpIdx !== undefined && cmpIdx !== null && gtmScript !== null)
    ? (cmpIdx < gtmScript ? 'LIKELY YES (CMP loads before GTM)' : 'LIKELY NO (GTM appears before CMP)')
    : 'UNKNOWN (could not determine)';
  report.push(`Order (CMP before GTM): ${orderMsg}`);

  // 5) Heuristic: Ad/Analytics scripts BEFORE consent? (should be no)
  const ga4Hard = idx(html, 'www.googletagmanager.com/gtag/js?id=G-');
  const adsenseHard = idx(html, 'pagead2.googlesyndication.com/pagead/js');
  report.push(`Hard-coded GA4 script tag before CMP: ${ga4Hard !== null && (cmpIdx===null || ga4Hard < cmpIdx) ? 'LIKELY YES' : 'No obvious hard-coded GA4 before CMP'}`);
  report.push(`Hard-coded AdSense script tag before CMP: ${adsenseHard !== null && (cmpIdx===null || adsenseHard < cmpIdx) ? 'LIKELY YES' : 'No obvious hard-coded AdSense before CMP'}`);

  // Output
  console.log('== CMP / Consent Mode Audit (HTML static) ==');
  report.forEach(r => console.log(' -', r));
  console.log('\nNotes:\n * This is a static HTML audit. Runtime consent & network behavior must be verified in the browser via GTM Preview and DevTools Network.');
})();

