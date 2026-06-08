document.addEventListener('DOMContentLoaded', function () {

    // ── Przełączanie widoków ──
    const tableSelect  = document.getElementById('table-select');
    const tableVisual  = document.getElementById('table-visual');
    const tableDetailed = document.getElementById('table-detailed');
    const tableFull    = document.getElementById('table-full');

    if (tableSelect) {
        tableSelect.addEventListener('change', function () {
            tableVisual.classList.remove('active');
            tableDetailed.classList.remove('active');
            tableFull.classList.remove('active');

            if (this.value === 'visual')   tableVisual.classList.add('active');
            if (this.value === 'detailed') tableDetailed.classList.add('active');
            if (this.value === 'full')     tableFull.classList.add('active');
        });
        createCustomSelect(tableSelect);
    }

    // ── Custom select dla nawigacji do albumu ──
    const albumSelect = document.getElementById('album-select');
    if (albumSelect) {
        createCustomSelect(albumSelect);
    }

    // ── Animacja przy przewijaniu ──
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.intro, .navigation, .content-section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });

    const tablesSection = document.querySelector('.tables-section');
    if (tablesSection) {
        tablesSection.style.opacity = '1';
        tablesSection.style.transform = 'translateY(0)';
        tablesSection.style.transition = 'none';
    }

    // ── Zamknij custom select po kliknięciu poza nim ──
    document.addEventListener('click', function () {
        document.querySelectorAll('.custom-select.open').forEach(el => el.classList.remove('open'));
    });
});


// ── Buduje custom dropdown na bazie natywnego <select> ──
function createCustomSelect(originalSelect) {
    if (!originalSelect) return;

    const wrapper = document.createElement('div');
    wrapper.className = 'custom-select';

    const trigger = document.createElement('div');
    trigger.className = 'custom-select__trigger';
    trigger.tabIndex = 0;
    wrapper.appendChild(trigger);

    const optionsBox = document.createElement('div');
    optionsBox.className = 'custom-select__options';
    wrapper.appendChild(optionsBox);

    // Wypełnij opcjami
    Array.from(originalSelect.options).forEach((opt, idx) => {
        // Pomiń opcje disabled (placeholder) — pokaż je tylko jako tekst triggera
        const optionEl = document.createElement('div');
        optionEl.className = 'custom-select__option';
        optionEl.textContent = opt.textContent;
        optionEl.dataset.value = opt.value;

        if (opt.disabled) {
            // Placeholder — nie dodawaj do listy opcji, tylko ustaw tekst triggera
            if (opt.selected) trigger.textContent = opt.textContent;
            return;
        }

        if (originalSelect.selectedIndex === idx) {
            optionEl.classList.add('selected');
            trigger.textContent = opt.textContent;
        }

        optionEl.addEventListener('click', function () {
            optionsBox.querySelectorAll('.custom-select__option').forEach(o => o.classList.remove('selected'));
            this.classList.add('selected');
            trigger.textContent = this.textContent;
            originalSelect.value = this.dataset.value;
            originalSelect.dispatchEvent(new Event('change', { bubbles: true }));
            wrapper.classList.remove('open');
        });

        optionsBox.appendChild(optionEl);
    });

    // Jeśli trigger nadal pusty — ustaw pierwszy tekst
    if (!trigger.textContent.trim()) {
        trigger.textContent = originalSelect.options[0]?.textContent || '';
    }

    // Otwieranie/zamykanie
    trigger.addEventListener('click', function (e) {
        e.stopPropagation();
        // Zamknij inne otwarte
        document.querySelectorAll('.custom-select.open').forEach(el => {
            if (el !== wrapper) el.classList.remove('open');
        });
        wrapper.classList.toggle('open');
    });

    // Obsługa klawiatury
    trigger.addEventListener('keydown', function (e) {
        const opts = Array.from(optionsBox.querySelectorAll('.custom-select__option'));
        const currentIndex = opts.findIndex(o => o.classList.contains('selected'));

        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            wrapper.classList.toggle('open');
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            const next = Math.min(opts.length - 1, currentIndex + 1);
            if (next !== currentIndex) {
                opts[currentIndex]?.classList.remove('selected');
                opts[next].classList.add('selected');
                trigger.textContent = opts[next].textContent;
                originalSelect.value = opts[next].dataset.value;
                originalSelect.dispatchEvent(new Event('change', { bubbles: true }));
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            const prev = Math.max(0, currentIndex - 1);
            if (prev !== currentIndex) {
                opts[currentIndex]?.classList.remove('selected');
                opts[prev].classList.add('selected');
                trigger.textContent = opts[prev].textContent;
                originalSelect.value = opts[prev].dataset.value;
                originalSelect.dispatchEvent(new Event('change', { bubbles: true }));
            }
        } else if (e.key === 'Escape') {
            wrapper.classList.remove('open');
        }
    });

    // Wstaw wrapper, ukryj oryginalny select
    originalSelect.style.display = 'none';
    originalSelect.parentNode.insertBefore(wrapper, originalSelect.nextSibling);
}


// ── Nawigacja do albumu ──
function przejdzDoAlbumu() {
    const select = document.getElementById('album-select');
    const url = select.value;
    if (!url) return;
    if (url.startsWith('http')) {
        window.open(url, '_blank');
    } else {
        window.location.href = url;
    }
}
