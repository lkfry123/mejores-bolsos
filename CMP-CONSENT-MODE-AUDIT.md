# CMP & Consent Mode v2 Audit Report

**Site:** https://affordable-handbags.com  
**GTM Container:** GTM-TCG7SMDD  
**Audit Date:** November 8, 2025

---

## 🔍 Executive Summary

The static HTML audit has been completed. The site currently **DOES NOT** have Consent Mode v2 implemented, which is required for GDPR compliance in the EEA, UK, and Switzerland.

---

## 📊 Audit Results (Live Homepage)

### ❌ **Critical Issues**

1. **No CMP (Consent Management Platform) detected**
   - No `__tcfapi`, OneTrust, Quantcast, Didomi, or other CMP references found
   
2. **No Consent Mode DEFAULT calls**
   - Missing `gtag('consent', 'default', {...})` initialization
   
3. **Missing Consent Mode v2 keys**
   - Required keys not found: `ad_user_data`, `ad_personalization`, `ad_storage`, `analytics_storage`
   
4. **AdSense loads before consent**
   - AdSense script (`pagead2.googlesyndication.com`) is hard-coded in `<head>` without consent checks
   - This may violate GDPR for EEA/UK/CH visitors

### ✅ **What's Working**

- GTM container (GTM-TCG7SMDD) is properly installed
- No hard-coded GA4 gtag.js detected (good - GTM should handle this)

---

## 🚨 Compliance Risk

**Current Risk Level:** **HIGH** for EEA/UK/CH visitors

### Why This Matters:

- **GDPR (EU):** Requires explicit consent before loading tracking/advertising cookies
- **UK GDPR:** Same requirements as EU GDPR
- **Swiss DPA:** Similar consent requirements
- **Google AdSense Policy:** Requires consent for personalized ads in EEA/UK

### Potential Consequences:

- GDPR fines (up to €20M or 4% of global revenue)
- AdSense account suspension for non-compliance
- User complaints
- Legal liability

---

## ✅ Recommended Solution: Implement Consent Mode v2

### Option 1: Google AdMob CMP (Free, Easy) - Formerly "Funding Choices"

**Best for:** Sites already using AdSense

**Setup via Google AdMob:**
1. Go to https://apps.admob.com/
2. Navigate to Privacy & messaging → EU consent
3. Create a consent message for GDPR compliance
4. Get your implementation code

**Implementation code structure:**

```html
<!-- Add BEFORE GTM snippet -->
<!-- Google AdMob CMP will automatically handle Consent Mode v2 -->
<script async src="https://fundingchoicesmessages.google.com/i/pub-8379967738924229?ers=1" nonce="YOUR_NONCE"></script>
<script nonce="YOUR_NONCE">(function() {function signalGooglefcPresent() {if (!window.frames['googlefcPresent']) {if (document.body) {const iframe = document.createElement('iframe'); iframe.style = 'width: 0; height: 0; border: none; z-index: -1000; left: -1000px; top: -1000px;'; iframe.style.display = 'none'; iframe.name = 'googlefcPresent'; document.body.appendChild(iframe);} else {setTimeout(signalGooglefcPresent, 0);}}}signalGooglefcPresent();})();</script>

<!-- Then add Consent Mode defaults -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  
  gtag('consent', 'default', {
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'ad_storage': 'denied',
    'analytics_storage': 'denied',
    'region': ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','CH','GB']
  });
  
  // For non-EEA regions, grant by default
  gtag('consent', 'default', {
    'ad_user_data': 'granted',
    'ad_personalization': 'granted',
    'ad_storage': 'granted',
    'analytics_storage': 'granted'
  });
</script>

<!-- THEN load GTM -->
```

**Note:** Google AdMob's consent solution integrates with the IAB Transparency & Consent Framework (TCF) and automatically updates consent signals.

### Option 2: Third-Party CMP

Popular options:
- **OneTrust** (Enterprise, comprehensive)
- **Cookiebot** (Mid-market)
- **Quantcast Choice** (Free for publishers)
- **Usercentrics** (European-focused)

---

## 🧪 Testing Tools Created

### 1. **Audit Script** (`tools/cmp-audit.mjs`)

Run anytime to check compliance:

```bash
node tools/cmp-audit.mjs
```

### 2. **Test Harness** (`tools/cmp-test.html`)

Local test page to verify consent behavior:

1. Open `tools/cmp-test.html` in browser
2. Enable GTM Preview mode
3. Click "Deny all" → Verify no tracking fires
4. Click "Grant all" → Verify tracking fires normally
5. Check DevTools Network tab for GA4/AdSense requests

**Or deploy to Netlify:**

```bash
# Copy to public path temporarily
cp tools/cmp-test.html cmp-test.html
# After deploy: https://affordable-handbags.com/cmp-test.html
```

---

## 📝 Implementation Checklist

- [ ] Choose a CMP solution (Google AdMob CMP recommended)
- [ ] Add Consent Mode v2 initialization BEFORE GTM
- [ ] Configure GTM tags to respect consent:
  - [ ] GA4 tag: Set "Consent Settings" → Require consent for ad_storage, analytics_storage
  - [ ] AdSense tags: Built-in consent checks (automatic with Consent Mode)
- [ ] Update AdSense script to load via GTM (not hard-coded)
- [ ] Test with `tools/cmp-test.html`
- [ ] Verify with GTM Preview in debug mode
- [ ] Test from EEA IP address (use VPN)
- [ ] Re-run `node tools/cmp-audit.mjs` to verify

---

## 🔗 Resources

- [Google Consent Mode v2 Guide](https://support.google.com/tagmanager/answer/10718549)
- [AdSense GDPR Compliance](https://support.google.com/adsense/answer/9803371)
- [Google AdMob Privacy & Messaging](https://support.google.com/admob/answer/10113207) (formerly Funding Choices)
- [GTM Consent Mode Implementation](https://developers.google.com/tag-platform/security/guides/consent)
- [IAB TCF v2.2 Framework](https://iabeurope.eu/tcf-2-0/)

---

## 📞 Next Steps

1. **Immediate:** Review this report with your compliance/legal team
2. **Short-term (1-2 weeks):** Implement Consent Mode v2 with chosen CMP
3. **Ongoing:** Monitor consent rates and adjust messaging for better UX

---

**Report Generated:** 2025-11-08  
**Tools Location:** `tools/cmp-audit.mjs`, `tools/cmp-test.html`

