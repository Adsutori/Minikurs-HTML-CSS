/* ============================================================
   PROGRESS.JS — Tracking postępu użytkownika
   Minikurs HTML5 i CSS3
   ============================================================ */

'use strict';

/* ============================================================
   AUTO-TRACKING — wysyła AJAX przy wejściu na stronę kursu
   ============================================================ */
(function initProgressTracking() {
  // Sprawdź czy jesteśmy na stronie kursu i czy jest meta tag z chapter
  const chapterMeta = document.querySelector('meta[name="chapter"]');
  if (!chapterMeta) return;

  const chapter = chapterMeta.getAttribute('content');
  if (!chapter) return;

  // Wyślij POST do backendu żeby oznaczyć rozdział jako odwiedzony
  const csrfToken = getCookie('csrftoken');

  fetch('/kurs/track-progress/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken':  csrfToken,
    },
    body: JSON.stringify({ chapter: chapter }),
    credentials: 'same-origin',
  })
  .then(function (response) {
    if (response.ok) return response.json();
  })
  .then(function (data) {
    if (data && data.progress_percent !== undefined) {
      updateSidebarProgress(data.progress_count, data.progress_percent);
    }
  })
  .catch(function () {
    // Cicho ignoruj błędy trackingu — nie psuj UX
  });
})();

/* ============================================================
   AKTUALIZACJA PROGRESS BARA W SIDEBARZE
   ============================================================ */
function updateSidebarProgress(count, percent) {
  const fill  = document.getElementById('sidebar-progress-fill');
  const text  = document.querySelector('.sidebar-progress-text');
  const pct   = document.querySelector('.sidebar-progress .text-right, .sidebar-progress div[style]');

  if (fill) {
    fill.style.width = percent + '%';
  }
  if (text) {
    text.textContent = count + '/13 rozdziałów';
  }
}

/* ============================================================
   DASHBOARD — animacja progress barów
   ============================================================ */
(function initDashboardProgress() {
  const dashFills = document.querySelectorAll('.dashboard-progress-fill');
  if (!dashFills.length) return;

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const target = entry.target.getAttribute('data-width');
          setTimeout(function () {
            entry.target.style.width = target + '%';
          }, 200);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.3 }
  );

  dashFills.forEach(function (fill) {
    fill.style.width = '0%';
    observer.observe(fill);
  });
})();

/* ============================================================
   HELPER — pobierz cookie (CSRF token)
   ============================================================ */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
