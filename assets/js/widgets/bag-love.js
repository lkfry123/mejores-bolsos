(function(){
document.addEventListener('DOMContentLoaded', () => {
try {
if (location.pathname !== '/') return;
  const TARGET_TEXT = 'Best Bags and Backpacks 2025: Expert Reviews & Shopping Guides';
  const h1 = Array.from(document.querySelectorAll('h1')).find(h => h.textContent.trim() === TARGET_TEXT);
  if (!h1) { console.warn('[bag-love] Target H1 not found on /'); return; }

  // Seasonal window: from NOW through Oct 31 inclusive, every year (browser time).
  function inRange(startMonth, startDay, endMonth, endDay){
    const now = new Date(); const y = now.getFullYear();
    const start = new Date(y, startMonth, startDay, 0,0,0);
    const end   = new Date(y, endMonth,   endDay,   23,59,59);
    return now >= start && now <= end;
  }
  // Activate from today's date to Oct 31 (inclusive)
  const isHalloweenWindow = inRange(new Date().getMonth(), new Date().getDate(), 9, 31);
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
  h1.parentNode.insertBefore(wrap, h1);

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

  // Shareable badge functions
  async function generateBadgeImage() {
    const badge = wrap.querySelector('.ah-love-badge');
    if (!badge || typeof html2canvas === 'undefined') return null;
    return await html2canvas(badge, { backgroundColor: null, scale: 2 });
  }

  async function downloadBadge() {
    const canvas = await generateBadgeImage();
    if (!canvas) return;
    const link = document.createElement('a');
    link.download = 'handbag-love.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
  }

  function shareToInstagram() {
    // Open Instagram app directly
    const shareUrl = `https://www.instagram.com/`;
    window.open(shareUrl, '_blank');
  }

  function shareToFacebook() {
    const shareText = 'Check out my handbag love score! 🎃';
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}&quote=${encodeURIComponent(shareText)}`;
    
    window.open(shareUrl, '_blank', 'width=600,height=400');
  }

  function shareToPinterest() {
    const shareText = 'My handbag love score! 🎃';
    const shareUrl = `https://pinterest.com/pin/create/button/?url=${encodeURIComponent(window.location.href)}&description=${encodeURIComponent(shareText)}`;
    
    window.open(shareUrl, '_blank', 'width=600,height=400');
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
