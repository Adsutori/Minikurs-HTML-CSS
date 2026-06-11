/* ============================================================
   LANDING.JS — Animacje landing page
   Minikurs HTML5 i CSS3
   ============================================================ */

'use strict';

/* ============================================================
   NAVBAR — efekt przy scrollu
   ============================================================ */
(function initNavScroll() {
  const nav = document.getElementById('landing-nav');
  if (!nav) return;

  window.addEventListener('scroll', function () {
    if (window.scrollY > 40) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }, { passive: true });
})();

/* ============================================================
   TYPING EFFECT — główne hasło hero
   ============================================================ */
(function initTypingEffect() {
  const target = document.getElementById('typed-text');
  if (!target) return;

  const text    = 'Naucz się budować strony internetowe';
  const speed   = 55;   // ms na znak
  const delay   = 600;  // opóźnienie startu
  let   index   = 0;

  function type() {
    if (index < text.length) {
      target.textContent += text.charAt(index);
      index++;
      setTimeout(type, speed);
    }
  }

  setTimeout(type, delay);
})();

// ============================================================
//  HERO PARTICLES — Neon-style animated grid + orbs
// ============================================================
(function () {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let W, H, particles = [], lines = [], mouse = { x: -9999, y: -9999 };
  const PARTICLE_COUNT = 80;
  const ACCENT = '124, 58, 237';
  const ACCENT2 = '168, 85, 247';

  function resize() {
    const parent = canvas.parentElement;
    W = canvas.width  = parent.offsetWidth;
    H = canvas.height = parent.offsetHeight || window.innerHeight;
  }

  window.addEventListener('resize', () => { resize(); init(); });

  // Śledzenie myszy
  canvas.closest('.hero')?.addEventListener('mousemove', e => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });
  canvas.closest('.hero')?.addEventListener('mouseleave', () => {
    mouse.x = -9999; mouse.y = -9999;
  });

  class Particle {
    constructor() { this.reset(true); }
    reset(initial = false) {
      this.x  = Math.random() * W;
      this.y  = initial ? Math.random() * H : H + 10;
      this.vx = (Math.random() - 0.5) * 0.3;
      this.vy = -(Math.random() * 0.4 + 0.1);
      this.size   = Math.random() * 1.5 + 0.5;
      this.alpha  = Math.random() * 0.5 + 0.1;
      this.color  = Math.random() > 0.5 ? ACCENT : ACCENT2;
      this.pulse  = Math.random() * Math.PI * 2;
      this.pulseSpeed = Math.random() * 0.02 + 0.01;
    }
    update() {
      // Przyciąganie do myszy
      const dx = mouse.x - this.x;
      const dy = mouse.y - this.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 120) {
        this.vx += dx / dist * 0.015;
        this.vy += dy / dist * 0.015;
      }
      this.vx *= 0.99;
      this.vy *= 0.99;
      this.x += this.vx;
      this.y += this.vy;
      this.pulse += this.pulseSpeed;
      if (this.y < -10) this.reset();
    }
    draw() {
      const a = this.alpha * (0.7 + 0.3 * Math.sin(this.pulse));
      // Glow
      const g = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 6);
      g.addColorStop(0, `rgba(${this.color}, ${a})`);
      g.addColorStop(1, `rgba(${this.color}, 0)`);
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size * 6, 0, Math.PI * 2);
      ctx.fillStyle = g;
      ctx.fill();
      // Core
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color}, ${Math.min(a * 2, 1)})`;
      ctx.fill();
    }
  }

  // Poziome linie skanujące (jak u Neon)
  class ScanLine {
    constructor() { this.reset(); }
    reset() {
      this.y     = Math.random() * H;
      this.speed = Math.random() * 0.3 + 0.1;
      this.alpha = Math.random() * 0.04 + 0.01;
      this.width = Math.random() * 200 + 100;
      this.x     = Math.random() * W;
    }
    update() {
      this.y -= this.speed;
      if (this.y < -2) { this.y = H + 2; this.x = Math.random() * W; }
    }
    draw() {
      const g = ctx.createLinearGradient(this.x - this.width / 2, 0, this.x + this.width / 2, 0);
      g.addColorStop(0,   `rgba(${ACCENT}, 0)`);
      g.addColorStop(0.5, `rgba(${ACCENT}, ${this.alpha})`);
      g.addColorStop(1,   `rgba(${ACCENT}, 0)`);
      ctx.beginPath();
      ctx.moveTo(this.x - this.width / 2, this.y);
      ctx.lineTo(this.x + this.width / 2, this.y);
      ctx.strokeStyle = g;
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }

  function connectParticles() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const d  = Math.sqrt(dx * dx + dy * dy);
        if (d < 100) {
          const a = (1 - d / 100) * 0.12;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(${ACCENT}, ${a})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function init() {
    particles = Array.from({ length: PARTICLE_COUNT }, () => new Particle());
    lines     = Array.from({ length: 8 }, () => new ScanLine());
  }

  function loop() {
    ctx.clearRect(0, 0, W, H);
    lines.forEach(l => { l.update(); l.draw(); });
    connectParticles();
    particles.forEach(p => { p.update(); p.draw(); });
    requestAnimationFrame(loop);
  }

  requestAnimationFrame(() => {
    resize();
    init();
    loop();
  });
})();


/* ============================================================
   ANIMOWANE LICZNIKI (counter przy scroll)
   ============================================================ */
(function initCounters() {
  const counters = document.querySelectorAll('.stat-number[data-target]');
  if (!counters.length) return;

  function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-target'), 10);
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = 1800;
    const start    = performance.now();

    function update(now) {
      const elapsed  = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // Easing: easeOutExpo
      const eased    = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      const current  = Math.round(eased * target);

      el.textContent = current + suffix;

      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }

    requestAnimationFrame(update);
  }

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  counters.forEach(function (counter) {
    observer.observe(counter);
  });
})();

/* ============================================================
   ACCORDION — program kursu
   ============================================================ */
(function initAccordion() {
  const items = document.querySelectorAll('.accordion-item');
  if (!items.length) return;

  items.forEach(function (item) {
    const header = item.querySelector('.accordion-header');
    if (!header) return;

    header.addEventListener('click', function () {
      const isOpen = item.classList.contains('open');

      // Zamknij wszystkie
      items.forEach(function (i) {
        i.classList.remove('open');
      });

      // Otwórz kliknięty (jeśli był zamknięty)
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });
})();

/* ============================================================
   SMOOTH SCROLL dla anchor linków
   ============================================================ */
(function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#') return;

      const target = document.querySelector(href);
      if (!target) return;

      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
})();

/* ============================================================
   FADE-IN przy scrollu (landing page)
   ============================================================ */
(function initLandingFadeIn() {
  const elements = document.querySelectorAll('.fade-in');
  if (!elements.length) return;

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  elements.forEach(function (el) { observer.observe(el); });
})();
