/* ============================================================
   MULTIMEDIA — Wspólny plik JavaScript
   Autor: Projekt edukacyjny
   Opis: Obsługa toggle kodu, kopiowania, nawigacji i smooth scroll
   ============================================================ */

/* ----------------------------------------------------------
   1. TOGGLE KODU
   Pokazuje lub ukrywa blok kodu po kliknięciu przycisku.
   Parametr: id — identyfikator bloku kodu (bez #)
   ---------------------------------------------------------- */
function toggleCode(id) {
  // Znajdź blok kodu o podanym id
  const blok = document.getElementById(id);
  if (!blok) return;

  // Znajdź przycisk toggle powiązany z tym blokiem
  // Szukamy przycisku z atrybutem data-toggle="id"
  const przycisk = document.querySelector(`[data-toggle="${id}"]`);

  // Przełącz widoczność przez klasę CSS
  const czyWidoczny = blok.classList.toggle('widoczny');

  // Zmień tekst przycisku
  if (przycisk) {
    przycisk.textContent = czyWidoczny ? '🙈 Ukryj kod' : '👁️ Pokaż kod';
  }
}

/* ----------------------------------------------------------
   2. KOPIOWANIE KODU
   Kopiuje zawartość bloku kodu do schowka systemowego.
   Parametr: id — identyfikator bloku kodu (bez #)
   ---------------------------------------------------------- */
function copyCode(id) {
  // Znajdź blok kodu
  const blok = document.getElementById(id);
  if (!blok) return;

  // Pobierz tekst z elementu <code> wewnątrz bloku
  const elementKodu = blok.querySelector('code');
  const tekst = elementKodu ? elementKodu.innerText : blok.innerText;

  // Znajdź przycisk kopiowania powiązany z tym blokiem
  const przycisk = document.querySelector(`[data-copy="${id}"]`);

  // Użyj nowoczesnego Clipboard API (wymaga HTTPS lub localhost)
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(tekst).then(() => {
      // Sukces — zmień tekst przycisku na 2 sekundy
      if (przycisk) {
        przycisk.textContent = 'Skopiowano ✓';
        przycisk.classList.add('skopiowano');
        setTimeout(() => {
          przycisk.textContent = '📋 Kopiuj kod';
          przycisk.classList.remove('skopiowano');
        }, 2000);
      }
    }).catch(() => {
      // Fallback jeśli Clipboard API zawiedzie
      kopiujFallback(tekst, przycisk);
    });
  } else {
    // Fallback dla starszych przeglądarek lub HTTP
    kopiujFallback(tekst, przycisk);
  }
}

/* ----------------------------------------------------------
   Fallback kopiowania przez tymczasowy element textarea
   ---------------------------------------------------------- */
function kopiujFallback(tekst, przycisk) {
  // Utwórz tymczasowy element textarea
  const obszar = document.createElement('textarea');
  obszar.value = tekst;
  obszar.style.position = 'fixed';
  obszar.style.left = '-9999px';
  obszar.style.top = '-9999px';
  document.body.appendChild(obszar);
  obszar.focus();
  obszar.select();

  try {
    // Stara metoda kopiowania
    document.execCommand('copy');
    if (przycisk) {
      przycisk.textContent = 'Skopiowano ✓';
      przycisk.classList.add('skopiowano');
      setTimeout(() => {
        przycisk.textContent = '📋 Kopiuj kod';
        przycisk.classList.remove('skopiowano');
      }, 2000);
    }
  } catch (err) {
    console.warn('Kopiowanie nie powiodło się:', err);
    if (przycisk) {
      przycisk.textContent = '❌ Błąd kopiowania';
      setTimeout(() => {
        przycisk.textContent = '📋 Kopiuj kod';
      }, 2000);
    }
  }

  // Usuń tymczasowy element
  document.body.removeChild(obszar);
}

/* ----------------------------------------------------------
   3. AKTYWNE PODŚWIETLENIE LINKU NAWIGACYJNEGO
   Dodaje klasę "active" do linku odpowiadającego bieżącej stronie.
   ---------------------------------------------------------- */
function oznaczAktywnyLink() {
  // Pobierz nazwę bieżącego pliku z URL
  const sciezka = window.location.pathname;
  const nazwaPliku = sciezka.split('/').pop() || 'index.html';

  // Znajdź wszystkie linki nawigacyjne
  const linki = document.querySelectorAll('.nav-linki a');

  linki.forEach(link => {
    // Pobierz href linku
    const href = link.getAttribute('href') || '';
    // Pobierz nazwę pliku z href
    const nazwaLinku = href.split('/').pop();

    // Usuń poprzednią klasę active
    link.classList.remove('active');

    // Porównaj nazwy plików
    if (nazwaLinku === nazwaPliku) {
      link.classList.add('active');
    }

    // Specjalny przypadek: strona główna
    if (
      (nazwaPliku === '' || nazwaPliku === 'index.html') &&
      (href === 'index.html' || href === '../index.html' || href === './' || href === '/')
    ) {
      link.classList.add('active');
    }
  });
}

/* ----------------------------------------------------------
   4. SMOOTH SCROLL dla kotwic wewnętrznych
   Płynne przewijanie do elementów z id po kliknięciu w link #id
   ---------------------------------------------------------- */
function inicjujSmoothScroll() {
  // Znajdź wszystkie linki wewnętrzne (zaczynające się od #)
  const linki = document.querySelectorAll('a[href^="#"]');

  linki.forEach(link => {
    link.addEventListener('click', function(zdarzenie) {
      const cel = document.querySelector(this.getAttribute('href'));
      if (cel) {
        zdarzenie.preventDefault();
        // Przewiń z uwzględnieniem stałego paska nawigacji
        const offsetNav = document.querySelector('.nav-glowna')?.offsetHeight || 0;
        const pozycja = cel.getBoundingClientRect().top + window.scrollY - offsetNav - 20;
        window.scrollTo({ top: pozycja, behavior: 'smooth' });
      }
    });
  });
}

/* ----------------------------------------------------------
   5. INICJALIZACJA — uruchom po załadowaniu DOM
   ---------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', function() {
  // Oznacz aktywny link w nawigacji
  oznaczAktywnyLink();

  // Inicjuj smooth scroll
  inicjujSmoothScroll();

  // Loguj informację o załadowaniu (pomocne przy debugowaniu)
  console.log('✅ Multimedia — skrypt załadowany pomyślnie.');
  console.log('📄 Bieżąca strona:', window.location.pathname);
});
