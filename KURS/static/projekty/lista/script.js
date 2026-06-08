document.querySelector('a[href="#home"]').addEventListener('click', function(e) {
    e.preventDefault();
    document.querySelector('.scroll-container').scrollTo({
    top: 0,
    behavior: 'smooth'
    });
});

function openPhoto(img) {
    const modal = document.getElementById("photoModal");
    const modalImage = document.getElementById("modalImage");
    const modalCaption = document.getElementById("modalCaption");
    const modalContent = modal.querySelector('.modal-content');

    modal.classList.remove('open');
    modal.style.display = "flex";
    void modal.offsetWidth;
    modal.classList.add('open');

    modalImage.src = img.src;
    modalImage.alt = img.alt || '';
    const desc = img.dataset.desc || img.alt || '';
    modalCaption.innerHTML = desc.replace(/\n/g, '<br>');
}

function closePhoto(event) {
    if (event.target.id === "photoModal") {
    closeWithAnimation();
    }
}

function closePhotoBtn(event) {
    event.stopPropagation();
    closeWithAnimation();
}

function closeWithAnimation() {
    const modal = document.getElementById("photoModal");
    if (!modal) return;
    const modalContent = modal.querySelector('.modal-content');

    let finished = false;
    const onContentEnd = function(e) {
    if (e.target === modalContent && (e.propertyName === 'transform' || e.propertyName === 'opacity' || e.propertyName === '-webkit-transform')) {
        finished = true;
        modal.style.display = "none";
        modalContent.removeEventListener('transitionend', onContentEnd);
    }
    };
    modalContent.addEventListener('transitionend', onContentEnd, { passive: true });

    modal.classList.remove('open');

    const root = getComputedStyle(document.documentElement);
    const dur = parseFloat(root.getPropertyValue('--modal-dur')) || 320;
    setTimeout(() => {
    if (!finished) {
        modal.style.display = "none";
        modalContent.removeEventListener('transitionend', onContentEnd);
    }
    }, dur + 120);
}