from django.apps import AppConfig


class MinikursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'minikurs'          # ← małe litery — to musi pasować do nazwy folderu
    verbose_name = 'Minikurs HTML5 i CSS3'
