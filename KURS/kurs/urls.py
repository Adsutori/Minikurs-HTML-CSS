from django.contrib import admin
from django.urls import path, include
from minikurs import views as minikurs_views

urlpatterns = [
    path('',       minikurs_views.landing, name='landing'),   # ← landing istnieje w views.py
    path('kurs/',  include('minikurs.urls')),
    path('admin/', admin.site.urls),
]
