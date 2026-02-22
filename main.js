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
