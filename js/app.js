/* ═══════════════════════════════════════════════════════════════════════
   JS & Node.js Elite Vault — Application Logic
   Features: Section switching, theme toggle, search, mermaid, scroll-to-top
   ═══════════════════════════════════════════════════════════════════════ */

// ── Section switching ──────────────────────────────────────────────────
let currentSection = 0;
const scrollPositions = {};

function showSection(idx) {
  // Save scroll for current section
  scrollPositions[currentSection] = window.scrollY;

  // Hide all sections
  document.querySelectorAll('.content-section').forEach(s => s.style.display = 'none');
  document.querySelectorAll('.toc-section').forEach(s => s.style.display = 'none');
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

  // Show selected
  const sec = document.getElementById('section-' + idx);
  const toc = document.getElementById('toc-' + idx);
  if (sec) sec.style.display = 'block';
  if (toc) toc.style.display = 'block';

  const btn = document.getElementById('nav-' + idx);
  if (btn) btn.classList.add('active');

  currentSection = idx;
  
  const targetScroll = scrollPositions[idx] || 0;
  window.scrollTo({ top: targetScroll, behavior: 'auto' });

  // Re-init mermaid for newly shown section
  requestAnimationFrame(() => {
    renderMermaidInSection(sec);
  });

  // Close mobile sidebar
  closeMobileSidebar();
}

// ── Mermaid Rendering ─────────────────────────────────────────────────
function getMermaidTheme() {
  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  if (isDark) {
    return {
      theme: 'dark',
      themeVariables: {
        primaryColor: '#1e293b',
        primaryTextColor: '#e2e8f0',
        primaryBorderColor: '#475569',
        lineColor: '#60a5fa',
        secondaryColor: '#1e3a5f',
        tertiaryColor: '#0f172a',
        fontFamily: 'JetBrains Mono, monospace',
        fontSize: '14px',
        nodeBorder: '#475569',
        mainBkg: '#1e293b',
        clusterBkg: '#0f172a',
        clusterBorder: '#475569',
        titleColor: '#e2e8f0',
        edgeLabelBackground: '#1e293b',
        nodeTextColor: '#e2e8f0',
      }
    };
  } else {
    return {
      theme: 'base',
      themeVariables: {
        primaryColor: '#dbeafe',
        primaryTextColor: '#1e293b',
        primaryBorderColor: '#93c5fd',
        lineColor: '#3b82f6',
        secondaryColor: '#eff6ff',
        tertiaryColor: '#f8fafc',
        fontFamily: 'JetBrains Mono, monospace',
        fontSize: '14px',
        nodeBorder: '#93c5fd',
        mainBkg: '#dbeafe',
        clusterBkg: '#eff6ff',
        clusterBorder: '#93c5fd',
        titleColor: '#1e293b',
        edgeLabelBackground: '#ffffff',
        nodeTextColor: '#1e293b',
      }
    };
  }
}

function renderMermaidInSection(sec) {
  if (typeof mermaid === 'undefined' || !sec) return;
  const unprocessed = sec.querySelectorAll('.mermaid[data-original]');
  unprocessed.forEach(el => {
    el.removeAttribute('data-processed');
    el.innerHTML = el.getAttribute('data-original');
  });
  try {
    mermaid.init(undefined, sec.querySelectorAll('.mermaid:not([data-processed])'));
  } catch(e) {
    console.warn('Mermaid render warning:', e);
  }
}

function reRenderAllMermaid() {
  if (typeof mermaid === 'undefined') return;
  const config = getMermaidTheme();
  mermaid.initialize({
    startOnLoad: false,
    ...config
  });
  // Re-render visible section
  const visibleSection = document.getElementById('section-' + currentSection);
  if (!visibleSection) return;

  const mermaids = visibleSection.querySelectorAll('.mermaid');
  mermaids.forEach(el => {
    if (el.getAttribute('data-original')) {
      el.removeAttribute('data-processed');
      el.innerHTML = el.getAttribute('data-original');
    }
  });

  try {
    mermaid.init(undefined, visibleSection.querySelectorAll('.mermaid:not([data-processed])'));
  } catch(e) {
    console.warn('Mermaid re-render warning:', e);
  }
}

// ── Copy code ─────────────────────────────────────────────────────────
function copyCode(btn) {
  const pre = btn.closest('.code-block-wrap').querySelector('pre');
  navigator.clipboard.writeText(pre.innerText).then(() => {
    btn.textContent = '✅';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = '📋'; btn.classList.remove('copied'); }, 1800);
  });
}

// ── Search ────────────────────────────────────────────────────────────
let searchTimeout;
function doSearch(query) {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    const q = query.trim().toLowerCase();
    if (!q) {
      // Remove all highlights
      document.querySelectorAll('.content-section').forEach(sec => {
        sec.querySelectorAll('mark').forEach(m => {
          m.replaceWith(document.createTextNode(m.textContent));
        });
      });
      return;
    }
    // Search across all sections
    document.querySelectorAll('.content-section').forEach((sec, idx) => {
      // Remove old marks first
      sec.querySelectorAll('mark').forEach(m => m.replaceWith(document.createTextNode(m.textContent)));

      const paragraphs = sec.querySelectorAll('p, .callout-body, h1, h2, h3, h4');
      let found = false;
      paragraphs.forEach(el => {
        const text = el.textContent;
        if (text.toLowerCase().includes(q)) {
          found = true;
          // Use a safer regex replace
          const escaped = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          el.innerHTML = el.innerHTML.replace(
            new RegExp(`(${escaped})`, 'gi'),
            '<mark>$1</mark>'
          );
        }
      });
      if (found) showSection(idx);
    });
  }, 300);
}

// ── Theme Toggle ──────────────────────────────────────────────────────
function getStoredTheme() {
  try { return localStorage.getItem('vault-theme'); } catch(e) { return null; }
}

function setStoredTheme(theme) {
  try { localStorage.setItem('vault-theme', theme); } catch(e) {}
}

function applyTheme(theme) {
  // Add transition class for smooth change
  document.documentElement.classList.add('theme-transitioning');

  document.documentElement.setAttribute('data-theme', theme);

  // Update theme button
  const btn = document.querySelector('.theme-btn');
  if (btn) btn.textContent = theme === 'dark' ? '🌙' : '☀️';

  // Switch highlight.js theme
  switchHighlightTheme(theme);

  // Re-render mermaid with new theme
  setTimeout(() => {
    reRenderAllMermaid();
    document.documentElement.classList.remove('theme-transitioning');
  }, 50);

  setStoredTheme(theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'dark';
  const next = current === 'dark' ? 'light' : 'dark';
  applyTheme(next);
}

function switchHighlightTheme(theme) {
  const existing = document.getElementById('hljs-theme');
  if (existing) existing.remove();

  const link = document.createElement('link');
  link.id = 'hljs-theme';
  link.rel = 'stylesheet';
  link.href = theme === 'dark'
    ? 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css'
    : 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css';
  document.head.appendChild(link);
}

// ── TOC active link on scroll ─────────────────────────────────────────
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      document.querySelectorAll('.toc-link').forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === '#' + id);
      });
    }
  });
}, { rootMargin: '-20% 0px -70% 0px' });

// ── Scroll to Top Button ──────────────────────────────────────────────
function initScrollToTop() {
  const btn = document.querySelector('.scroll-top-btn');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ── Reading Progress Bar ──────────────────────────────────────────────
function initProgressBar() {
  const bar = document.querySelector('.reading-progress-bar');
  if (!bar) return;

  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    bar.style.width = progress + '%';
  }, { passive: true });
}

// ── Mobile Sidebar ────────────────────────────────────────────────────
function toggleMobileSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');
  if (sidebar) sidebar.classList.toggle('open');
  if (overlay) overlay.classList.toggle('visible');
}

function closeMobileSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');
  if (sidebar) sidebar.classList.remove('open');
  if (overlay) overlay.classList.remove('visible');
}

// ── Store original mermaid sources before rendering ────────────────────
function storeOriginalMermaid() {
  document.querySelectorAll('.mermaid').forEach(el => {
    if (!el.getAttribute('data-original')) {
      el.setAttribute('data-original', el.innerHTML);
    }
  });
}

// ── Init ──────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Apply stored theme or default
  const storedTheme = getStoredTheme() || 'dark';
  document.documentElement.setAttribute('data-theme', storedTheme);
  const thBtn = document.querySelector('.theme-btn');
  if (thBtn) thBtn.textContent = storedTheme === 'dark' ? '🌙' : '☀️';

  // Switch highlight.js theme based on stored theme
  switchHighlightTheme(storedTheme);

  // Activate first nav button
  const firstBtn = document.getElementById('nav-0');
  if (firstBtn) firstBtn.classList.add('active');

  // highlight.js
  if (typeof hljs !== 'undefined') {
    document.querySelectorAll('pre code').forEach(el => hljs.highlightElement(el));
  }

  // Store original mermaid content before first render
  storeOriginalMermaid();

  // mermaid initialization
  if (typeof mermaid !== 'undefined') {
    const config = getMermaidTheme();
    mermaid.initialize({
      startOnLoad: false,
      ...config
    });
  }

  // Observe headings for TOC
  document.querySelectorAll('h1[id], h2[id], h3[id], h4[id]').forEach(h => observer.observe(h));

  // Init scroll-to-top
  initScrollToTop();

  // Init progress bar
  initProgressBar();

  // Setup mobile overlay click
  const overlay = document.querySelector('.sidebar-overlay');
  if (overlay) {
    overlay.addEventListener('click', closeMobileSidebar);
  }

  // Wire up theme toggle button
  if (thBtn) thBtn.addEventListener('click', toggleTheme);

  // Initial show section 0 to trigger mermaid and layout
  showSection(0);
});
