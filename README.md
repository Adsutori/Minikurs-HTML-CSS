# Minikurs HTML5 i CSS3

Projekt szkolny — kompletny kurs HTML5 i CSS3 zbudowany w Django.

## 🚀 Uruchomienie

```bash
# 1. Sklonuj repozytorium
git clone <url>
cd minikurs

# 2. Utwórz środowisko wirtualne
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate.bat     # Windows

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Wykonaj migracje
python manage.py migrate

# 5. Uruchom serwer
python manage.py runserver
