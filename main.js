/* ── Mobile Nav ─────────────────────────────────────────────────────────── */
const hamburgerBtn = document.getElementById('hamburgerBtn');
const mobileNav = document.getElementById('mobileNav');
const mobileNavClose = document.getElementById('mobileNavClose');
const mobileNavOverlay = document.getElementById('mobileNavOverlay');

function openMobileNav() {
  mobileNav.classList.add('open');
  hamburgerBtn.classList.add('open');
  hamburgerBtn.setAttribute('aria-expanded', 'true');
  document.body.style.overflow = 'hidden';
}
function closeMobileNav() {
  mobileNav.classList.remove('open');
  hamburgerBtn.classList.remove('open');
  hamburgerBtn.setAttribute('aria-expanded', 'false');
  document.body.style.overflow = '';
}

hamburgerBtn.addEventListener('click', openMobileNav);
mobileNavClose.addEventListener('click', closeMobileNav);
mobileNavOverlay.addEventListener('click', closeMobileNav);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMobileNav(); });

/* ── Booking Modal ──────────────────────────────────────────────────────── */
function openBookingModal(e) {
  if (e) e.preventDefault();
  const modal = document.getElementById('bookingModal');
  modal.classList.add('modal--open');
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  setTimeout(() => document.getElementById('fullName').focus(), 100);
}
function closeBookingModal() {
  const modal = document.getElementById('bookingModal');
  modal.classList.remove('modal--open');
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

// Wire all booking trigger elements
document.querySelectorAll('[data-action="book"]').forEach(el => {
  el.addEventListener('click', openBookingModal);
});

// Wire all close trigger elements
document.querySelectorAll('[data-action="close-modal"]').forEach(el => {
  el.addEventListener('click', closeBookingModal);
});

// Escape key closes modal
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeBookingModal(); });

/* HIPAA NOTE: When connecting to a real backend, post form data only to a
   HIPAA-compliant endpoint (EMR API or secure healthcare form processor).
   Never transmit PHI via standard email protocols. */
document.getElementById('bookingForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const btn = this.querySelector('button[type="submit"]');
  btn.textContent = '✓ Appointment Requested!';
  btn.style.background = '#10b981';
  setTimeout(() => {
    this.reset();
    btn.textContent = 'Request Appointment';
    btn.style.background = '';
    closeBookingModal();
  }, 2000);
});

/* ── Scroll Animations ──────────────────────────────────────────────────── */
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -60px 0px' };
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = 'running';
      entry.target.classList.add('in-view');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

function prepareScrollAnim(el, animName, delay = 0) {
  const rect = el.getBoundingClientRect();
  const inViewport = rect.top < window.innerHeight && rect.bottom > 0;
  if (inViewport) return;
  el.style.opacity = '0';
  el.style.animation = `${animName} 0.7s ease-out ${delay}s forwards paused`;
  observer.observe(el);
}

document.querySelectorAll('.section-head h2, .section-head p').forEach(el => {
  prepareScrollAnim(el, 'slideInFromBottom');
});
document.querySelectorAll('.review-card, .loc-card, .art-card').forEach((card, i) => {
  prepareScrollAnim(card, 'slideInFromBottom', i * 0.08);
});
document.querySelectorAll('.svc-card').forEach((card, i) => {
  const anim = i === 0 ? 'slideInLeft' : i === 2 ? 'slideInRight' : 'slideInFromBottom';
  prepareScrollAnim(card, anim);
});
document.querySelectorAll('.award-pill').forEach((pill, i) => {
  prepareScrollAnim(pill, 'slideInFromBottom', i * 0.07);
});

/* ── Video Filter (videos.html) ─────────────────────────────────────────── */
if (document.querySelector('.filter-btn')) {
  function filterVideos(category, btn) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const sections = {
      sinus:   document.getElementById('section-sinus'),
      sleep:   document.getElementById('section-sleep'),
      allergy: document.getElementById('section-allergy'),
      ear:     document.getElementById('section-ear')
    };
    const featured = document.getElementById('section-featured');
    if (category === 'all') {
      if (featured) featured.style.display = '';
      Object.values(sections).forEach(s => { if (s) s.style.display = ''; });
    } else {
      if (featured) featured.style.display = 'none';
      Object.entries(sections).forEach(([key, sec]) => {
        if (sec) sec.style.display = key === category ? '' : 'none';
      });
    }
    const target = category === 'all' ? featured : sections[category];
    if (target) setTimeout(() => target.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
  }
  document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => filterVideos(btn.dataset.filter, btn));
  });
}

/* ── Contact Form ───────────────────────────────────────────────────────── */
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const btn = this.querySelector('button[type="submit"]');
    btn.textContent = '✓ Request Submitted!';
    btn.style.background = '#10b981';
    setTimeout(() => {
      this.reset();
      btn.textContent = 'Submit Request';
      btn.style.background = '';
    }, 3000);
  });
}

/* ── BSP FAQ Accordion (balloon-sinuplasty.html) ────────────────────────── */
document.querySelectorAll('.bfaq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    // Collapse all others
    document.querySelectorAll('.bfaq-q[aria-expanded="true"]').forEach(other => {
      if (other !== btn) {
        other.setAttribute('aria-expanded', 'false');
        other.nextElementSibling.style.maxHeight = null;
      }
    });
    // Toggle current
    btn.setAttribute('aria-expanded', String(!expanded));
    const panel = btn.nextElementSibling;
    panel.style.maxHeight = expanded ? null : panel.scrollHeight + 'px';
  });
});

/* ── Smooth scroll for anchor links ────────────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const href = link.getAttribute('href');
    if (href !== '#' && document.querySelector(href)) {
      e.preventDefault();
      document.querySelector(href).scrollIntoView({ behavior: 'smooth' });
    }
  });
});

/* ── Cedar Season Banner (homepage, Nov–Feb) ────────────────────────────── */
(function () {
  const m = new Date().getMonth(); // 0=Jan … 11=Dec
  const isCedarSeason = m === 10 || m === 11 || m === 0 || m === 1; // Nov, Dec, Jan, Feb
  if (!isCedarSeason) return;
  if (sessionStorage.getItem('cedarDismissed')) return;
  const banner = document.getElementById('cedarBanner');
  if (!banner) return;
  banner.style.display = 'block';
  const closeBtn = document.getElementById('cedarBannerClose');
  if (closeBtn) {
    closeBtn.addEventListener('click', function () {
      banner.style.display = 'none';
      sessionStorage.setItem('cedarDismissed', '1');
    });
  }
}());

/* ── Cedar Season Section (allergy page, Oct–Feb) ───────────────────────── */
(function () {
  const m = new Date().getMonth(); // 0=Jan … 11=Dec
  const isCedar = m === 9 || m === 10 || m === 11 || m === 0 || m === 1; // Oct–Feb
  if (!isCedar) return;
  const section = document.getElementById('allergycedarSeasonSection');
  if (section) section.style.display = '';
}());

/* ── FAQ Page (faq.html) ─────────────────────────────────────────────────── */
(function () {
  /* Accordion */
  const faqQs = document.querySelectorAll('.faq-q');
  if (!faqQs.length) return; // not on FAQ page

  faqQs.forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      // Collapse all others
      document.querySelectorAll('.faq-q[aria-expanded="true"]').forEach(other => {
        if (other !== btn) {
          other.setAttribute('aria-expanded', 'false');
          other.nextElementSibling.style.maxHeight = null;
        }
      });
      btn.setAttribute('aria-expanded', String(!expanded));
      const panel = btn.nextElementSibling;
      panel.style.maxHeight = expanded ? null : panel.scrollHeight + 'px';
    });
  });

  /* Category filter */
  document.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.cat;
      document.querySelectorAll('.faq-group').forEach(group => {
        group.dataset.hidden = (cat !== 'all' && group.dataset.cat !== cat) ? 'true' : 'false';
      });
      const searchEl = document.getElementById('faqSearch');
      if (searchEl) searchEl.value = '';
      const countEl = document.getElementById('searchCount');
      if (countEl) countEl.textContent = '';
      // Reset item visibility
      document.querySelectorAll('.faq-item').forEach(item => { item.dataset.hidden = 'false'; });
      checkNoResults();
    });
  });

  /* Search */
  const searchInput = document.getElementById('faqSearch');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const q = this.value.trim().toLowerCase();
      if (q) {
        document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
        const allBtn = document.querySelector('.cat-btn[data-cat="all"]');
        if (allBtn) allBtn.classList.add('active');
        document.querySelectorAll('.faq-group').forEach(g => { g.dataset.hidden = 'false'; });
      }
      let totalVisible = 0;
      document.querySelectorAll('.faq-item').forEach(item => {
        if (!q) { item.dataset.hidden = 'false'; totalVisible++; return; }
        const text = item.textContent.toLowerCase();
        const match = text.includes(q);
        item.dataset.hidden = match ? 'false' : 'true';
        if (match) totalVisible++;
      });
      document.querySelectorAll('.faq-group').forEach(group => {
        if (!q) { group.dataset.hidden = 'false'; return; }
        const hasVisible = [...group.querySelectorAll('.faq-item')].some(i => i.dataset.hidden !== 'true');
        group.dataset.hidden = hasVisible ? 'false' : 'true';
      });
      const countEl = document.getElementById('searchCount');
      if (countEl) countEl.textContent = q ? totalVisible + ' question' + (totalVisible !== 1 ? 's' : '') + ' found' : '';
      checkNoResults();
    });
  }

  function checkNoResults() {
    const anyVisible = [...document.querySelectorAll('.faq-group')].some(g => g.dataset.hidden !== 'true');
    const noRes = document.getElementById('noResults');
    if (noRes) noRes.style.display = anyVisible ? 'none' : 'block';
  }

  /* Sidebar scroll-spy */
  const groups = document.querySelectorAll('.faq-group[id]');
  const sideLinks = document.querySelectorAll('.faq-sidebar-nav a');
  if (groups.length && sideLinks.length) {
    const faqObs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          sideLinks.forEach(l => l.classList.remove('active'));
          const match = document.querySelector('.faq-sidebar-nav a[href="#' + entry.target.id + '"]');
          if (match) match.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    groups.forEach(g => faqObs.observe(g));
  }
}());
