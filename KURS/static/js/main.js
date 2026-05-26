/* ============================================================
   MAIN.JS — Globalne skrypty
   Minikurs HTML5 i CSS3
   ============================================================ */

'use strict';

/* ============================================================
   HAMBURGER MENU (mobile sidebar)
   ============================================================ */
(function initHamburger() {
  const hamburger = document.getElementById('hamburger');
  const sidebar   = document.getElementById('sidebar');
  const overlay   = document.getElementById('sidebar-overlay');

  if (!hamburger || !sidebar) return;

  function openSidebar() {
    sidebar.classList.add('open');
    overlay && overlay.classList.add('active');
    hamburger.classList.add('active');
    hamburger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay && overlay.classList.remove('active');
    hamburger.classList.remove('active');
    hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  hamburger.addEventListener('click', function () {
    if (sidebar.classList.contains('open')) {
      closeSidebar();
    } else {
      openSidebar();
    }
  });

  overlay && overlay.addEventListener('click', closeSidebar);

  // Zamknij sidebar przy resize do desktop
  window.addEventListener('resize', function () {
    if (window.innerWidth > 768) {
      closeSidebar();
    }
  });
})();

/* ============================================================
   FADE-IN przy scrollu (IntersectionObserver)
   ============================================================ */
(function initFadeIn() {
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

  elements.forEach(function (el) {
    observer.observe(el);
  });
})();

/* ============================================================
   TABLE OF CONTENTS — aktywna sekcja (IntersectionObserver)
   ============================================================ */
(function initTOC() {
  const tocLinks = document.querySelectorAll('.toc-list a');
  if (!tocLinks.length) return;

  const sections = [];
  tocLinks.forEach(function (link) {
    const id = link.getAttribute('href').replace('#', '');
    const section = document.getElementById(id);
    if (section) sections.push(section);
  });

  if (!sections.length) return;

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          tocLinks.forEach(function (link) {
            link.classList.remove('toc-active');
            if (link.getAttribute('href') === '#' + entry.target.id) {
              link.classList.add('toc-active');
            }
          });
        }
      });
    },
    { threshold: 0.3, rootMargin: '-64px 0px -50% 0px' }
  );

  sections.forEach(function (section) {
    observer.observe(section);
  });
})();

/* ============================================================
   PROGRESS BAR — animacja przy ładowaniu
   ============================================================ */
(function initProgressBars() {
  const fills = document.querySelectorAll('.progress-bar-fill');
  if (!fills.length) return;

  // Krótkie opóźnienie żeby animacja była widoczna
  setTimeout(function () {
    fills.forEach(function (fill) {
      const target = fill.style.width;
      fill.style.width = '0%';
      setTimeout(function () {
        fill.style.width = target;
      }, 100);
    });
  }, 300);
})();

/* ============================================================
   RANGE INPUT — wyświetlanie wartości
   ============================================================ */
(function initRangeInputs() {
  const ranges = document.querySelectorAll('input[type="range"][data-output]');
  ranges.forEach(function (range) {
    const outputId = range.getAttribute('data-output');
    const output   = document.getElementById(outputId);
    if (!output) return;

    output.textContent = range.value;
    range.addEventListener('input', function () {
      output.textContent = this.value;
    });
  });
})();

/* ============================================================
   DJANGO MESSAGES — auto-dismiss po 5s
   ============================================================ */
(function initMessages() {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      alert.style.opacity    = '0';
      alert.style.transform  = 'translateY(-8px)';
      setTimeout(function () {
        alert.remove();
      }, 500);
    }, 5000);
  });
})();
