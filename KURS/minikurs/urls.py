# minikurs/urls.py  ← plik w folderze aplikacji

from django.urls import path
from . import views

app_name = 'minikurs'

urlpatterns = [
    path('',                              views.glowna,                    name='glowna'),
    path('html/',                         views.html_poradnik,             name='html'),
    path('css/',                          views.css_poradnik,              name='css'),
    path('sprawdzian/',                   views.sprawdzian,                name='sprawdzian'),
    path('lista/',                        views.lista,                     name='lista'),
    path('tabela-kolorow/',               views.tabela_kolorow,            name='tabela_kolorow'),
    path('tabele-listy-lacza/',           views.tabele_listy_lacza,        name='tabele_listy_lacza'),
    path('multimedia/',                   views.multimedia,                name='multimedia'),
    path('formularze/resumo/',            views.formularze_resumo,         name='formularze_resumo'),
    path('formularze/kwestionariusz/',    views.formularze_kwestionariusz, name='formularze_kwestionariusz'),
    path('o-mnie/',                       views.o_mnie,                    name='o_mnie'),
    path('linki/',                        views.linki,                     name='linki'),
    path('kontakt/',                      views.kontakt,                   name='kontakt'),
    path('dashboard/',                    views.dashboard,                 name='dashboard'),
    path('certyfikat/<uuid:cert_id>/',    views.certyfikat,                name='certyfikat'),
    path('zapisz-sie/<str:course>/',      views.enroll,                    name='enroll'),
    path('login/',                        views.login_view,                name='login'),
    path('logout/',                       views.logout_view,               name='logout'),
    path('register/',                     views.register_view,             name='register'),
    path('track-progress/',               views.track_progress_ajax,       name='track_progress'),
]
