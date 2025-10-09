(function(){
document.addEventListener('DOMContentLoaded', () => {
try {
console.log('[bag-love] Widget script loaded');
console.log('[bag-love] Current pathname:', location.pathname);
if (location.pathname !== '/') { console.log('[bag-love] Not on homepage, skipping'); return; }
  const TARGET_TEXT = 'Best Bags and Backpacks 2025: Expert Reviews & Shopping Guides';
  const h1 = Array.from(document.querySelectorAll('h1')).find(h => h.textContent.trim() === TARGET_TEXT);
  console.log('[bag-love] Found H1:', h1);
  if (!h1) { console.warn('[bag-love] Target H1 not found on /'); return; }

  // Seasonal window: from NOW through Oct 31 inclusive, every year (browser time).
  function inRange(startMonth, startDay, endMonth, endDay){
    const now = new Date(); const y = now.getFullYear();
    const start = new Date(y, startMonth, startDay, 0,0,0);
    const end   = new Date(y, endMonth,   endDay,   23,59,59);
    return now >= start && now <= end;
  }
  // Activate from today's date to Oct 31 (inclusive)
  const now = new Date();
  const isHalloweenWindow = inRange(now.getMonth(), now.getDate(), 9, 31);
  console.log('[bag-love] Current date:', now);
  console.log('[bag-love] Is Halloween window:', isHalloweenWindow);
  document.documentElement.classList.toggle('is-halloween-window', isHalloweenWindow);

  const ICONS = {
    pumpkin: '/assets/img/widgets/pumpkin.svg',
    bat:     '/assets/img/widgets/bat.svg',
    ghost:   '/assets/img/widgets/ghost.svg'
  };
  function getHalloweenRemark(v){
    if (v <= 20) return { text:"Looks like you'd rather carry a pumpkin than a purse… 🎃", icon:ICONS.pumpkin, alt:'pumpkin' };
    if (v <= 40) return { text:"Half-hearted handbag haunter 👻", icon:ICONS.ghost, alt:'ghost' };
    if (v <= 70) return { text:"Wickedly stylish! 🦇 Your bag obsession is taking flight.", icon:ICONS.bat, alt:'bat' };
    if (v <= 90) return { text:"You're under a handbag spell ✨👜", icon:ICONS.pumpkin, alt:'pumpkin' };
    return           { text:"Full moon handbag fanatic — the spirits approve! 🌕👜", icon:ICONS.bat, alt:'bat' };
  }

  const wrap = document.createElement('section');
  wrap.className = 'ah-love-wrap' + (isHalloweenWindow ? ' is-halloween' : '');
  wrap.innerHTML = `
    <div class="ah-love-header">
      <span class="ah-emoji">${isHalloweenWindow ? '🎃' : '👜'}</span>
      <span>How much do you love bags?</span>
    </div>
    <div class="ah-love-control">
      <input type="range" min="0" max="100" step="1" value="60" aria-label="How much do you love bags" />
      <div class="ah-love-value" aria-live="polite" role="status">60%</div>
    </div>

    <div class="ah-love-caption">
      <span class="ah-love-remark" aria-live="polite"></span>
    </div>

    <div class="ah-love-badge">
      <div class="ah-badge-title">Handbag Love</div>
      <div class="ah-badge-score">60% ${isHalloweenWindow ? '🎃' : '👜'}</div>
      <div class="ah-badge-remark">
        <span class="ah-badge-remark-text"></span>
      </div>
      <div class="ah-badge-footer">Affordable-Handbags.com</div>
    </div>

    <div class="ah-love-share">
      <div class="ah-share-label">
        <span class="ah-share-text">Share</span>
        <span class="ah-share-arrow">↗</span>
      </div>
      <div class="ah-share-buttons">
        <button type="button" class="ah-social-btn instagram" data-platform="instagram" title="Share on Instagram">
          📷
        </button>
        <button type="button" class="ah-social-btn facebook" data-platform="facebook" title="Share on Facebook">
          f
        </button>
        <button type="button" class="ah-social-btn pinterest" data-platform="pinterest" title="Share on Pinterest">
          📌
        </button>
      </div>
    </div>

    <noscript>Tell us how much you love bags.</noscript>
  `;
  console.log('[bag-love] Inserting widget before H1');
  h1.parentNode.insertBefore(wrap, h1);
  console.log('[bag-love] Widget inserted successfully');

  const pageKey = 'ah_bag_love:' + location.pathname;
  const input   = wrap.querySelector('input[type="range"]');
  const valueEl = wrap.querySelector('.ah-love-value');

  const remarkEl = wrap.querySelector('.ah-love-remark');
  const bScore   = wrap.querySelector('.ah-badge-score');
  const bRemarkT = wrap.querySelector('.ah-badge-remark-text');

  // Init from localStorage
  const saved = localStorage.getItem(pageKey);
  if (saved !== null) input.value = String(saved);

  function sync(){
    const v = Number(input.value);
    wrap.style.setProperty('--pos', v);
    valueEl.textContent = `${v}%`;

    if (isHalloweenWindow){
      const { text } = getHalloweenRemark(v);
      remarkEl.textContent = text;
      if (bScore) bScore.textContent = `${v}% 🎃`;
      if (bRemarkT) bRemarkT.textContent = text;
    } else {
      remarkEl.textContent = 'Show your bag-lover energy!';
      if (bScore) bScore.textContent = `${v}% 👜`;
      if (bRemarkT) bRemarkT.textContent = '';
    }

    window.dispatchEvent(new CustomEvent('AH_BAG_LOVE', { detail:{ value:v, page:location.pathname }}));
  }

  input.addEventListener('input', sync);
  input.addEventListener('change', () => {
    localStorage.setItem(pageKey, String(input.value));
  });

  // Shareable badge image generation removed to avoid iOS download prompts

  function shareToInstagram() {
    // Open Instagram app directly
    const shareUrl = `https://www.instagram.com/`;
    window.open(shareUrl, '_blank');
  }

  function shareToFacebook() {
    const canonicalEl = document.querySelector('link[rel="canonical"]');
    const pageUrl = canonicalEl && canonicalEl.href ? canonicalEl.href : window.location.href;
    // Use mobile sharer endpoint; omit quote for maximum compatibility
    const shareUrl = `https://m.facebook.com/sharer.php?u=${encodeURIComponent(pageUrl)}`;
    const isMobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    if (isMobile) {
      window.location.href = shareUrl; // same-tab navigation avoids popup blockers on mobile
      return;
    }
    const a = document.createElement('a');
    a.href = shareUrl;
    a.target = '_blank';
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  function shareToPinterest() {
    const v = Number(input.value);
    const shareText = `My handbag love score: ${v}% ${isHalloweenWindow ? '🎃' : '👜'}`;
    const canonicalEl = document.querySelector('link[rel="canonical"]');
    const pageUrl = canonicalEl && canonicalEl.href ? canonicalEl.href : window.location.href;
    // Use standard create endpoint and let Pinterest scrape OG image; more stable across iOS Safari
    const shareUrl = `https://www.pinterest.com/pin/create/button/?url=${encodeURIComponent(pageUrl)}&description=${encodeURIComponent(shareText)}`;
    const isMobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    if (isMobile) {
      window.location.href = shareUrl; // same-tab navigation for iOS Safari
      return;
    }
    const a = document.createElement('a');
    a.href = shareUrl;
    a.target = '_blank';
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  // Event listeners for share buttons
  const socialBtns = wrap.querySelectorAll('.ah-social-btn');
  socialBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const platform = btn.dataset.platform;
      
      switch(platform) {
        case 'instagram':
          shareToInstagram();
          break;
        case 'facebook':
          shareToFacebook();
          break;
        case 'pinterest':
          shareToPinterest();
          break;
      }
    });
  });

  // initial sync
  sync();
} catch (e){
  console.error('[bag-love] error:', e);
}
});
})();
