from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import uuid

from .models import Enrollment, ChapterProgress, Certificate


# ================================================================
# LANDING — publiczna
# ================================================================
def landing(request):
    if request.user.is_authenticated:
        return redirect('minikurs:glowna')
    return render(request, 'index.html')


# ================================================================
# AUTH — publiczne, własny layout
# ================================================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('minikurs:glowna')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '')
            return redirect(next_url if next_url else 'minikurs:glowna')
        else:
            messages.error(request, 'Nieprawidłowa nazwa użytkownika lub hasło.')

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('landing')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('minikurs:glowna')

    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username:
            messages.error(request, 'Nazwa użytkownika jest wymagana.')
        elif len(username) < 3:
            messages.error(request, 'Nazwa użytkownika musi mieć min. 3 znaki.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ta nazwa użytkownika jest już zajęta.')
        elif password1 != password2:
            messages.error(request, 'Hasła nie są zgodne.')
        elif len(password1) < 8:
            messages.error(request, 'Hasło musi mieć min. 8 znaków.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
            )
            login(request, user)
            messages.success(request, f'Witaj, {username}! Konto zostało utworzone.')
            return redirect('minikurs:glowna')

    return render(request, 'auth/register.html')


# ================================================================
# HELPER
# ================================================================
def _track(request, slug):
    if request.user.is_authenticated:
        ChapterProgress.objects.get_or_create(
            user=request.user,
            chapter=slug,
        )


# ================================================================
# KURS — wszystkie widoki chronione @login_required
# ================================================================
@login_required
def glowna(request):
    _track(request, 'glowna')
    return render(request, 'kurs/glowna.html')


@login_required
def html_poradnik(request):
    _track(request, 'html')
    return render(request, 'kurs/html_poradnik.html')


@login_required
def css_poradnik(request):
    _track(request, 'css')
    return render(request, 'kurs/css_poradnik.html')


@login_required
def sprawdzian(request):
    _track(request, 'sprawdzian')
    return render(request, 'kurs/sprawdzian.html')


@login_required
def lista(request):
    _track(request, 'lista')
    return render(request, 'kurs/lista.html')


@login_required
def tabela_kolorow(request):
    _track(request, 'tabela_kolorow')
    return render(request, 'kurs/tabela_kolorow.html')


@login_required
def tabele_listy_lacza(request):
    _track(request, 'tabele_listy_lacza')
    return render(request, 'kurs/tabele_listy_lacza.html')


@login_required
def multimedia(request):
    _track(request, 'multimedia')
    return render(request, 'kurs/multimedia.html')


@login_required
def formularze_resumo(request):
    _track(request, 'formularze_resumo')
    return render(request, 'kurs/formularze_resumo.html')


@login_required
def formularze_kwestionariusz(request):
    _track(request, 'formularze_kwestionariusz')
    return render(request, 'kurs/formularze_kwestionariusz.html')


@login_required
def o_mnie(request):
    _track(request, 'o_mnie')
    return render(request, 'kurs/o_mnie.html')


@login_required
def linki(request):
    _track(request, 'linki')
    return render(request, 'kurs/linki.html')


@login_required
def kontakt(request):
    _track(request, 'kontakt')
    return render(request, 'kurs/kontakt.html')


# ================================================================
# DASHBOARD
# ================================================================
@login_required
def dashboard(request):
    enrollments  = Enrollment.objects.filter(user=request.user)
    progress     = ChapterProgress.objects.filter(
                       user=request.user
                   ).order_by('-visited_at')[:20]
    certificates = Certificate.objects.filter(enrollment__user=request.user)

    all_chapters   = ChapterProgress.CHAPTER_CHOICES
    visited_slugs  = set(
        ChapterProgress.objects.filter(
            user=request.user
        ).values_list('chapter', flat=True)
    )
    progress_count = len(visited_slugs)
    total_chapters = len(all_chapters)
    progress_pct   = round(progress_count / total_chapters * 100) if total_chapters else 0

    enrolled_keys     = set(enrollments.values_list('course', flat=True))
    available_courses = [
        (k, v) for k, v in Enrollment.COURSE_CHOICES
        if k not in enrolled_keys
    ]

    return render(request, 'kurs/dashboard.html', {
        'enrollments':       enrollments,
        'progress':          progress,
        'certificates':      certificates,
        'progress_count':    progress_count,
        'progress_percent':  progress_pct,
        'available_courses': available_courses,
        'total_chapters':    total_chapters,
    })


# ================================================================
# CERTYFIKAT
# ================================================================
@login_required
def certyfikat(request, cert_id):
    cert = get_object_or_404(
        Certificate,
        certificate_id=cert_id,
        enrollment__user=request.user
    )
    return render(request, 'kurs/certyfikat.html', {'cert': cert})


# ================================================================
# ENROLL
# ================================================================
@login_required
def enroll(request, course):
    valid = [k for k, _ in Enrollment.COURSE_CHOICES]
    if course not in valid:
        messages.error(request, 'Nieznany kurs.')
        return redirect('minikurs:dashboard')

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
    )
    if created:
        messages.success(request, f'Zapisano na: {enrollment.get_course_display()}')
    else:
        messages.info(request, 'Jesteś już zapisany na ten kurs.')

    return redirect('minikurs:dashboard')


# ================================================================
# AJAX TRACKING
# ================================================================
@require_POST
def track_progress_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'skip'})

    try:
        data    = json.loads(request.body)
        chapter = data.get('chapter', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'status': 'error'}, status=400)

    valid = [k for k, _ in ChapterProgress.CHAPTER_CHOICES]
    if chapter not in valid:
        return JsonResponse({'status': 'skip'})

    _, created = ChapterProgress.objects.get_or_create(
        user=request.user,
        chapter=chapter,
    )
    return JsonResponse({'status': 'created' if created else 'exists'})
