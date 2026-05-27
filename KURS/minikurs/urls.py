from django.urls import path
from . import views

app_name = 'minikurs'

urlpatterns = [

    # ── O kursie (strona główna po zalogowaniu) ──────────────
    path('',                              views.glowna,                     name='glowna'),

    # ── Dashboard ────────────────────────────────────────────
    path('dashboard/',                    views.dashboard,                  name='dashboard'),

    # ── Poradniki ─────────────────────────────────────────────
    path('html/',                         views.html_poradnik,              name='html'),
    path('css/',                          views.css_poradnik,               name='css'),

    # ── Projekty ──────────────────────────────────────────────
    path('sprawdzian/',                   views.sprawdzian,                 name='sprawdzian'),
    path('lista/',                        views.lista,                      name='lista'),
    path('tabela-kolorow/',               views.tabela_kolorow,             name='tabela_kolorow'),
    path('tabele-listy-lacza/',           views.tabele_listy_lacza,         name='tabele_listy_lacza'),
    path('multimedia/',                   views.multimedia,                 name='multimedia'),
    path('formularze/resumo/',            views.formularze_resumo,          name='formularze_resumo'),
    path('formularze/kwestionariusz/',    views.formularze_kwestionariusz,  name='formularze_kwestionariusz'),

    # ── Strony osobiste ───────────────────────────────────────
    path('o-mnie/',                       views.o_mnie,                     name='o_mnie'),
    path('linki/',                        views.linki,                      name='linki'),
    path('kontakt/',                      views.kontakt,                    name='kontakt'),

    # ── Certyfikat ────────────────────────────────────────────
    path('certyfikat/<uuid:cert_id>/',    views.certyfikat,                 name='certyfikat'),

    # ── Kurs — zapisy ─────────────────────────────────────────
    path('zapisz-sie/<str:course>/',      views.enroll,                     name='enroll'),

    # ── AJAX ──────────────────────────────────────────────────
    path('track/',                        views.track_progress_ajax,        name='track_progress'),
]
