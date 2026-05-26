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

/* ============================================================
   CANVAS PARTICLES — pływające cząsteczki w tle hero
   ============================================================ */
(function initParticles() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let   W, H, particles;

  // Kolory cząsteczek
  const COLORS = [
    'rgba(124, 58, 237, 0.6)',
    'rgba(168, 85, 247, 0.4)',
    'rgba(109, 40, 217, 0.5)',
    'rgba(196, 181, 253, 0.3)',
  ];

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function createParticle() {
    return {
      x:      Math.random() * W,
      y:      Math.random() * H,
      r:      Math.random() * 2.5 + 0.5,
      dx:     (Math.random() - 0.5) * 0.4,
      dy:     (Math.random() - 0.5) * 0.4,
      color:  COLORS[Math.floor(Math.random() * COLORS.length)],
      alpha:  Math.random() * 0.7 + 0.2,
      pulse:  Math.random() * Math.PI * 2,
      pulseSpeed: Math.random() * 0.02 + 0.005,
    };
  }

  function initParticleArray() {
    const count = Math.min(Math.floor((W * H) / 12000), 120);
    particles   = Array.from({ length: count }, createParticle);
  }

  function drawParticle(p) {
    p.pulse += p.pulseSpeed;
    const currentAlpha = p.alpha * (0.7 + 0.3 * Math.sin(p.pulse));

    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = p.color.replace(/[\d.]+\)$/, currentAlpha + ')');
    ctx.fill();
  }

  function connectParticles() {
    const maxDist = 120;
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx   = particles[i].x - particles[j].x;
        const dy   = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < maxDist) {
          const opacity = (1 - dist / maxDist) * 0.15;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(124, 58, 237, ${opacity})`;
          ctx.lineWidth   = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, W, H);

    particles.forEach(function (p) {
      p.x += p.dx;
      p.y += p.dy;

      // Odbicie od krawędzi
      if (p.x < -10) p.x = W + 10;
      if (p.x > W + 10) p.x = -10;
      if (p.y < -10) p.y = H + 10;
      if (p.y > H + 10) p.y = -10;

      drawParticle(p);
    });

    connectParticles();
    requestAnimationFrame(animate);
  }

  resize();
  initParticleArray();
  animate();

  window.addEventListener('resize', function () {
    resize();
    initParticleArray();
  }, { passive: true });
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
