import json
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Enrollment, Progress, Certificate


# ============================================================
# HELPER — pobierz kontekst progressu dla sidebar
# ============================================================
def get_progress_context(user):
    """Zwraca słownik z danymi postępu do kontekstu szablonu."""
    if not user.is_authenticated:
        return {}

    count   = Progress.objects.filter(user=user).count()
    percent = round((count / 13) * 100)
    return {
        'progress_count':   count,
        'progress_percent': percent,
    }


def track_chapter(user, chapter):
    """Tworzy lub aktualizuje rekord Progress dla danego rozdziału."""
    if user.is_authenticated and chapter:
        Progress.objects.get_or_create(user=user, chapter=chapter)


# ============================================================
# LANDING PAGE
# ============================================================
def landing(request):
    return render(request, 'index.html')


# ============================================================
# STRONA GŁÓWNA KURSU
# ============================================================
def glowna(request):
    track_chapter(request.user, 'glowna')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/glowna.html', ctx)


# ============================================================
# PORADNIK HTML
# ============================================================
def html_poradnik(request):
    track_chapter(request.user, 'html')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/html_poradnik.html', ctx)


# ============================================================
# PORADNIK CSS
# ============================================================
def css_poradnik(request):
    track_chapter(request.user, 'css')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/css_poradnik.html', ctx)


# ============================================================
# SPRAWDZIAN
# ============================================================
def sprawdzian(request):
    track_chapter(request.user, 'sprawdzian')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/sprawdzian.html', ctx)


# ============================================================
# LISTA
# ============================================================
def lista(request):
    track_chapter(request.user, 'lista')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/lista.html', ctx)


# ============================================================
# TABELA KOLORÓW
# ============================================================
def tabela_kolorow(request):
    track_chapter(request.user, 'tabela_kolorow')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/tabela_kolorow.html', ctx)


# ============================================================
# TABELE, LISTY, ŁĄCZA
# ============================================================
def tabele_listy_lacza(request):
    track_chapter(request.user, 'tabele_listy_lacza')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/tabele_listy_lacza.html', ctx)


# ============================================================
# MULTIMEDIA
# ============================================================
def multimedia(request):
    track_chapter(request.user, 'multimedia')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/multimedia.html', ctx)


# ============================================================
# FORMULARZE — RESUMO
# ============================================================
def formularze_resumo(request):
    track_chapter(request.user, 'formularze_resumo')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/formularze_resumo.html', ctx)


# ============================================================
# FORMULARZE — KWESTIONARIUSZ
# ============================================================
def formularze_kwestionariusz(request):
    track_chapter(request.user, 'formularze_kwestionariusz')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/formularze_kwestionariusz.html', ctx)


# ============================================================
# O MNIE
# ============================================================
def o_mnie(request):
    track_chapter(request.user, 'o_mnie')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/o_mnie.html', ctx)


# ============================================================
# LINKI
# ============================================================
def linki(request):
    track_chapter(request.user, 'linki')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/linki.html', ctx)


# ============================================================
# KONTAKT
# ============================================================
def kontakt(request):
    track_chapter(request.user, 'kontakt')
    ctx = get_progress_context(request.user)
    return render(request, 'kurs/kontakt.html', ctx)


# ============================================================
# DASHBOARD
# ============================================================
@login_required(login_url='/kurs/login/')
def dashboard(request):
    user        = request.user
    enrollments = Enrollment.objects.filter(user=user)
    progress    = Progress.objects.filter(user=user).order_by('-visited_at')
    certs       = Certificate.objects.filter(user=user)

    count   = progress.count()
    percent = round((count / 13) * 100)

    # Dostępne kursy do zapisu
    enrolled_courses = [e.course for e in enrollments]
    available_courses = [
        c for c in Enrollment.COURSE_CHOICES
        if c[0] not in enrolled_courses
    ]

    ctx = {
        'enrollments':       enrollments,
        'progress':          progress[:10],  # ostatnie 10
        'certificates':      certs,
        'progress_count':    count,
        'progress_percent':  percent,
        'available_courses': available_courses,
    }
    return render(request, 'kurs/dashboard.html', ctx)


# ============================================================
# CERTYFIKAT
# ============================================================
def certyfikat(request, cert_id):
    cert = get_object_or_404(Certificate, certificate_id=cert_id)
    ctx  = {
        'cert':             cert,
        'progress_count':   get_progress_context(request.user).get('progress_count', 0),
        'progress_percent': get_progress_context(request.user).get('progress_percent', 0),
    }
    return render(request, 'kurs/certyfikat.html', ctx)


# ============================================================
# ZAPISZ SIĘ NA KURS
# ============================================================
@login_required(login_url='/kurs/login/')
def enroll(request, course):
    valid_courses = [c[0] for c in Enrollment.COURSE_CHOICES]
    if course not in valid_courses:
        messages.error(request, 'Nieznany kurs.')
        return redirect('kurs:dashboard')

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
    )
    if created:
        messages.success(request, f'Zapisano na kurs: {enrollment.get_course_display()}!')
    else:
        messages.info(request, 'Jesteś już zapisany na ten kurs.')

    return redirect('kurs:dashboard')


# ============================================================
# TRACK PROGRESS — endpoint AJAX
# ============================================================
@require_POST
def track_progress_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'skip'}, status=200)

    try:
        data    = json.loads(request.body)
        chapter = data.get('chapter', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'status': 'error'}, status=400)

    valid_chapters = [c[0] for c in Progress.CHAPTER_CHOICES]
    if chapter not in valid_chapters:
        return JsonResponse({'status': 'invalid'}, status=400)

    Progress.objects.get_or_create(user=request.user, chapter=chapter)

    count   = Progress.objects.filter(user=request.user).count()
    percent = round((count / 13) * 100)

    # Sprawdź czy ukończono wszystkie rozdziały → wystaw certyfikat
    if count >= 13:
        enrollment, _ = Enrollment.objects.get_or_create(
            user=request.user,
            course='full',
        )
        if not enrollment.completed:
            enrollment.completed    = True
            enrollment.completed_at = datetime.now()
            enrollment.save()
            Certificate.objects.get_or_create(
                user=request.user,
                enrollment=enrollment,
            )

    return JsonResponse({
        'status':           'ok',
        'progress_count':   count,
        'progress_percent': percent,
    })


# ============================================================
# LOGOWANIE
# ============================================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('kurs:glowna')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'kurs:glowna')
            messages.success(request, f'Witaj, {user.username}! 👋')
            return redirect(next_url)
        else:
            messages.error(request, 'Nieprawidłowa nazwa użytkownika lub hasło.')

    return render(request, 'kurs/login.html')


# ============================================================
# WYLOGOWANIE
# ============================================================
def logout_view(request):
    logout(request)
    messages.info(request, 'Zostałeś wylogowany.')
    return redirect('landing')


# ============================================================
# REJESTRACJA
# ============================================================
def register_view(request):
    if request.user.is_authenticated:
        return redirect('kurs:glowna')

    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # Walidacja
        if not username or not password1:
            messages.error(request, 'Nazwa użytkownika i hasło są wymagane.')
        elif password1 != password2:
            messages.error(request, 'Hasła nie są identyczne.')
        elif len(password1) < 8:
            messages.error(request, 'Hasło musi mieć co najmniej 8 znaków.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ta nazwa użytkownika jest już zajęta.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
            )
            login(request, user)
            messages.success(request, f'Konto utworzone! Witaj, {username}! 🎉')
            return redirect('kurs:glowna')

    return render(request, 'kurs/register.html')
