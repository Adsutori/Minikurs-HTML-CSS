from django.contrib import admin
from django.urls import path, include
from minikurs import views as v

urlpatterns = [
    # Landing — publiczna
    path('',        v.landing,       name='landing'),

    # Auth — publiczne, własny layout
    path('login/',    v.login_view,    name='login'),
    path('logout/',   v.logout_view,   name='logout'),
    path('register/', v.register_view, name='register'),

    # Kurs — chroniony
    path('kurs/',   include('minikurs.urls')),

    path('admin/',  admin.site.urls),
]
