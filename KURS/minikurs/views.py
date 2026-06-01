from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from minikurs.models import Course, Lesson, Enrollment, LessonProgress
from .models import Course, Lesson, Enrollment, LessonProgress


# ================================================================
# LANDING — publiczna
# ================================================================
def landing(request):
    if request.user.is_authenticated:
        return redirect('minikurs:glowna')
    return render(request, 'index.html')


# ================================================================
# AUTH
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
# HELPER — tracking odwiedzin (uproszczony, bez ChapterProgress)
# ================================================================
def _track(request, slug):
    """Oznacza lekcję jako odwiedzoną jeśli istnieje w nowym systemie."""
    if request.user.is_authenticated:
        lesson = Lesson.objects.filter(slug=slug).first()
        if lesson:
            LessonProgress.objects.get_or_create(
                user=request.user,
                lesson=lesson,
            )


# ================================================================
# STRONY KURSU — chronione @login_required
# ================================================================
@login_required
def glowna(request):
    course_chapters = [
        ('01', 'Wprowadzenie do HTML',      'Struktura, znaczniki, DOCTYPE',         'code-2',        'html'),
        ('02', 'Poradnik HTML5',            'Semantyka, formularze, multimedia',     'file-code',     'html'),
        ('03', 'Poradnik CSS3',             'Selektory, Flexbox, Grid, animacje',    'paintbrush',    'css'),
        ('04', 'Sprawdzian',                'Sprawdź swoją wiedzę',                  'clipboard-check','sprawdzian'),
        ('05', 'Lista zadań',               'Projekt: interaktywna lista',           'list-checks',   'lista'),
        ('06', 'Tabela kolorów',            'Projekt: paleta barw CSS',              'palette',       'tabela_kolorow'),
        ('07', 'Tabele, Listy, Łącza',      'Projekt: strona z tabelami',            'table-2',       'tabele_listy_lacza'),
        ('08', 'Multimedia',                'Projekt: galeria i wideo',              'film',          'multimedia'),
        ('09', 'Resumo',                    'Projekt: CV w HTML/CSS',                'file-text',     'formularze_resumo'),
        ('10', 'Kwestionariusz',            'Projekt: formularz kontaktowy',         'clipboard',     'formularze_kwestionariusz'),
        ('11', 'O mnie',                    'Projekt: strona osobista',              'user',          'o_mnie'),
        ('12', 'Linki',                     'Zasoby i materiały dodatkowe',          'external-link', 'linki'),
        ('13', 'Kontakt',                   'Formularz kontaktowy',                  'mail',          'kontakt'),
    ]
    return render(request, 'kurs/glowna.html', {
        'course_chapters': course_chapters,
    })


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
    # Wszystkie enrollmenty — active=True
    enrollments = Enrollment.objects.filter(
        user=request.user, active=True
    ).select_related('course').order_by('course__order')

    enrollments_data = []
    total_done = 0
    total_all  = 0

    for enrollment in enrollments:
        lessons_count = enrollment.course.get_lessons().count()
        done_count    = LessonProgress.objects.filter(
            user=request.user,
            lesson__course=enrollment.course,
            completed=True
        ).count()
        total_done += done_count
        total_all  += lessons_count
        enrollments_data.append({
            'enrollment':    enrollment,
            'lessons_count': lessons_count,
            'done_count':    done_count,
            'progress':      enrollment.progress_percent(),
        })

    # Ostatnia aktywność — 15 ostatnich wpisów
    recent_progress = LessonProgress.objects.filter(
        user=request.user
    ).select_related('lesson__course').order_by('-visited_at')[:15]

    # Kursy dostępne (niezapisane lub active=False)
    enrolled_course_ids = Enrollment.objects.filter(
        user=request.user, active=True
    ).values_list('course_id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_course_ids)

    # Globalny procent
    global_percent = round((total_done / total_all) * 100) if total_all else 0

    return render(request, 'kurs/dashboard.html', {
        'enrollments_data':  enrollments_data,
        'recent_progress':   recent_progress,
        'available_courses': available_courses,
        'global_percent':    global_percent,
        'total_done':        total_done,
        'total_all':         total_all,
        'certificates':      [],   # podłącz gdy będzie model Certificate
    })


# ================================================================
# CERTYFIKAT (zachowany ze starego kodu)
# ================================================================
@login_required
def certyfikat(request, cert_id):
    # Jeśli masz model Certificate — zostaw
    # Jeśli usunąłeś — zakomentuj ten widok i URL
    try:
        from .models import Certificate
        cert = get_object_or_404(
            Certificate,
            certificate_id=cert_id,
            enrollment__user=request.user
        )
        return render(request, 'kurs/certyfikat.html', {'cert': cert})
    except ImportError:
        return redirect('minikurs:dashboard')


# ================================================================
# KURSY — lista i szczegół
# ================================================================
@login_required
def kursy_lista(request):
    courses = Course.objects.all()
    enrolled_ids = Enrollment.objects.filter(
        user=request.user, active=True
    ).values_list('course_id', flat=True)

    courses_data = []
    for course in courses:
        enrollment = Enrollment.objects.filter(
            user=request.user, course=course, active=True
        ).first()
        courses_data.append({
            'course':        course,
            'enrolled':      course.id in enrolled_ids,
            'enrollment':    enrollment,
            'progress':      enrollment.progress_percent() if enrollment else 0,
            'lessons_count': course.get_lessons().count(),
        })

    return render(request, 'kurs/kursy_lista.html', {'courses_data': courses_data})


@login_required
def kurs_detail(request, course_slug):
    course     = get_object_or_404(Course, slug=course_slug)
    enrollment = Enrollment.objects.filter(
        user=request.user, course=course, active=True
    ).first()

    lessons = course.get_lessons()

    user_progress = {
        lp.lesson_id: lp
        for lp in LessonProgress.objects.filter(
            user=request.user, lesson__course=course
        )
    }

    lessons_data = []
    for lesson in lessons:
        lp = user_progress.get(lesson.id)
        lessons_data.append({
            'lesson':    lesson,
            'visited':   lp is not None,
            'completed': lp.completed if lp else False,
        })

    return render(request, 'kurs/kurs_detail.html', {
        'course':       course,
        'enrollment':   enrollment,
        'lessons_data': lessons_data,
        'progress':     enrollment.progress_percent() if enrollment else 0,
        'done_count':   enrollment.completed_count() if enrollment else 0,
    })


# ================================================================
# LEKCJA
# ================================================================
@login_required
def lekcja(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, published=True)

    # Sprawdź czy użytkownik jest zapisany — jeśli nie, przekieruj
    enrollment = Enrollment.objects.filter(
        user=request.user, course=course, active=True
    ).first()
    if not enrollment:
        messages.warning(request, f'Musisz zapisać się na kurs „{course.title}", aby przeglądać lekcje.')
        return redirect('minikurs:kurs_detail', course_slug=course_slug)

    # Zapisz postęp odwiedzin
    progress, _ = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
    )
    LessonProgress.objects.filter(pk=progress.pk).update(visited_at=timezone.now())

    lessons       = list(course.get_lessons())
    current_index = next((i for i, l in enumerate(lessons) if l.pk == lesson.pk), 0)
    prev_lesson   = lessons[current_index - 1] if current_index > 0 else None
    next_lesson   = lessons[current_index + 1] if current_index < len(lessons) - 1 else None

    total = len(lessons)
    done  = LessonProgress.objects.filter(
        user=request.user,
        lesson__course=course,
        completed=True
    ).count()
    course_progress = round((done / total) * 100) if total else 0

    return render(request, lesson.template, {
        'course':          course,
        'lesson':          lesson,
        'enrollment':      enrollment,
        'prev_lesson':     prev_lesson,
        'next_lesson':     next_lesson,
        'lessons':         lessons,
        'progress':        progress,
        'course_progress': course_progress,
        'done_count':      done,
        'total_count':     total,
    })



@login_required
def toggle_complete(request, course_slug, lesson_slug):
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
        lp, _  = LessonProgress.objects.get_or_create(
            user=request.user, lesson=lesson
        )
        lp.completed    = not lp.completed
        lp.completed_at = timezone.now() if lp.completed else None
        lp.save()
    return redirect('minikurs:lekcja', course_slug=course_slug, lesson_slug=lesson_slug)


# ================================================================
# ENROLL / UNENROLL
# ================================================================
@login_required
def enroll(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'active': True}
    )
    if not enrollment.active:
        enrollment.active = True
        enrollment.save(update_fields=['active'])

    if created:
        messages.success(request, f'Zapisano na kurs „{course.title}"!')
    else:
        messages.info(request, f'Jesteś już zapisany na kurs „{course.title}".')

    return redirect('minikurs:kurs_detail', course_slug=course_slug)  # ← była zła nazwa



@login_required
def unenroll(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    # Usuń cały postęp lekcji dla tego kursu
    deleted_count, _ = LessonProgress.objects.filter(
        user=request.user,
        lesson__course=course
    ).delete()

    # Dezaktywuj enrollment
    Enrollment.objects.filter(
        user=request.user, course=course
    ).update(active=False)

    messages.info(
        request,
        f'Zrezygnowano z kursu „{course.title}". '
        f'Usunięto postęp ({deleted_count} lekcji).'
    )
    return redirect('minikurs:kursy_lista')



# ================================================================
# AJAX TRACKING (zachowany, teraz używa LessonProgress)
# ================================================================
@require_POST
def track_progress_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'skip'})

    try:
        data = json.loads(request.body)
        slug = data.get('chapter', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'status': 'error'}, status=400)

    lesson = Lesson.objects.filter(slug=slug).first()
    if not lesson:
        return JsonResponse({'status': 'invalid'})  # ← brakowało return

    lp, _ = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
    )

    return JsonResponse({'status': 'ok'})



@login_required
def complete_lesson(request, course_slug, lesson_slug):
    """Oznacz lekcję jako ukończoną — POST only."""
    if request.method != 'POST':
        return redirect('minikurs:lekcja', course_slug=course_slug, lesson_slug=lesson_slug)

    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)

    progress, _ = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
    )
    if not progress.completed:
        progress.completed    = True
        progress.completed_at = timezone.now()
        progress.save(update_fields=['completed', 'completed_at', 'visited_at'])

    # Przekieruj do następnej lekcji lub z powrotem
    lessons       = list(course.get_lessons())
    current_index = next((i for i, l in enumerate(lessons) if l.pk == lesson.pk), 0)

    if current_index < len(lessons) - 1:
        next_lesson = lessons[current_index + 1]
        return redirect('minikurs:lekcja',
                        course_slug=course_slug,
                        lesson_slug=next_lesson.slug)

    return redirect('minikurs:kurs', course_slug=course_slug)