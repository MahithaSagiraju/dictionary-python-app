const form = document.getElementById('searchForm');
const status = document.getElementById('status');
const spinner = document.getElementById('spinner');
const searchBtn = document.getElementById('searchBtn');

form?.addEventListener('submit', (e)=>{
  status.textContent = 'Searching…';
  if (spinner) spinner.setAttribute('aria-hidden', 'false');
  if (searchBtn) searchBtn.disabled = true;
});

// Re-enable UI when user focuses input again
const input = document.getElementById('word');
input?.addEventListener('input', ()=>{
  status.textContent = '';
  if (spinner) spinner.setAttribute('aria-hidden', 'true');
  if (searchBtn) searchBtn.disabled = false;
});

// Dark mode toggle
const darkToggle = document.getElementById('darkToggle');
function applyTheme(theme){
  if (theme === 'dark') document.documentElement.classList.add('dark');
  else document.documentElement.classList.remove('dark');
}

const saved = localStorage.getItem('theme') || 'light';
applyTheme(saved);

darkToggle?.addEventListener('click', ()=>{
  const now = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
  applyTheme(now);
  localStorage.setItem('theme', now);
});

// Add small entrance animation for images when they load
document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('.images img').forEach((img, i)=>{
    img.style.opacity = '0';
    img.style.transform = 'translateY(6px)';
    img.onload = ()=>{
      setTimeout(()=>{
        img.style.transition = 'opacity .5s ease, transform .5s cubic-bezier(.2,.9,.2,1)';
        img.style.opacity = '1';
        img.style.transform = 'none';
      }, i*80);
    };
    // if already cached
    if (img.complete) img.onload();
  });

  // subtle header animation
  requestAnimationFrame(()=>document.body.classList.add('ready'));
});
