from django.db import models
from django.contrib.auth.models import User
import uuid


class Enrollment(models.Model):
    COURSE_CHOICES = [
        ('html_css', 'HTML5 i CSS3 — Podstawy'),
        ('html_adv', 'HTML5 — Zaawansowany'),
        ('css_adv',  'CSS3 — Zaawansowany'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course      = models.CharField(max_length=20, choices=COURSE_CHOICES)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed   = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name        = 'Zapis na kurs'
        verbose_name_plural = 'Zapisy na kursy'

    def __str__(self):
        return f'{self.user.username} → {self.get_course_display()}'


class ChapterProgress(models.Model):
    CHAPTER_CHOICES = [
        ('glowna',                   '🏠 Strona główna kursu'),
        ('html',                     '📖 HTML — Poradnik'),
        ('css',                      '🎨 CSS — Poradnik'),
        ('sprawdzian',               '✅ Sprawdzian'),
        ('lista',                    '📋 Lista'),
        ('tabela_kolorow',           '🎨 Tabela kolorów'),
        ('tabele_listy_lacza',       '🔗 Tabele, Listy i Łącza'),
        ('multimedia',               '🎬 Multimedia'),
        ('formularze_resumo',        '📄 Formularz CV'),
        ('formularze_kwestionariusz','📋 Kwestionariusz'),
        ('o_mnie',                   '👤 O mnie'),
        ('linki',                    '🔗 Linki'),
        ('kontakt',                  '📞 Kontakt'),
    ]

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chapter_progress')
    chapter    = models.CharField(max_length=40, choices=CHAPTER_CHOICES)
    visited_at = models.DateTimeField(auto_now=True)
    completed  = models.BooleanField(default=False)

    class Meta:
        unique_together     = ('user', 'chapter')
        verbose_name        = 'Postęp rozdziału'
        verbose_name_plural = 'Postępy rozdziałów'
        ordering            = ['-visited_at']

    def __str__(self):
        return f'{self.user.username} — {self.get_chapter_display()}'


class Certificate(models.Model):
    enrollment     = models.OneToOneField(Enrollment, on_delete=models.CASCADE,
                                          related_name='certificate')
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    issued_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Certyfikat'
        verbose_name_plural = 'Certyfikaty'

    def __str__(self):
        return f'Certyfikat {self.certificate_id} — {self.enrollment}'
