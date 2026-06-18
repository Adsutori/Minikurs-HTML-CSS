# 🎓 Minikurs HTML/CSS

Interaktywna platforma edukacyjna do nauki HTML i CSS, zbudowana w Django.  
Zawiera lekcje, projekty, quizy oraz system certyfikatów.

---

## 📋 Wymagania

- Windows 10 lub 11
- Połączenie z internetem (tylko przy pierwszej instalacji)

---

## 🌐 Wersja online

Projekt dostępny również online: **https://minikurs-html-css.onrender.com**

---

## 🚀 Szybki start (zalecane)

Jeśli nie chcesz nic robić ręcznie — **kliknij dwukrotnie `URUCHOM.bat`**  
i postępuj zgodnie z instrukcjami na ekranie.

Bat automatycznie:
- zainstaluje Pythona (jeśli nie jest zainstalowany)
- utworzy wirtualne środowisko
- zainstaluje wszystkie biblioteki
- wykona migracje bazy danych
- załaduje dane (kursy, lekcje)
- uruchomi serwer

Po zakończeniu otwórz przeglądarkę i wejdź na: **http://127.0.0.1:8000/**

---

## 🔧 Instalacja ręczna (krok po kroku)

### Krok 1 — Zainstaluj Python

1. Wejdź na https://www.python.org/downloads/
2. Pobierz **Python 3.12** (lub nowszy)
3. Uruchom instalator
4. ⚠️ **WAŻNE:** Zaznacz opcję **„Add Python to PATH"** przed kliknięciem Install
5. Kliknij **„Install Now"**
6. Po instalacji zamknij instalator

Sprawdź czy działa — otwórz `cmd` i wpisz:
```
python --version
```
Powinno pokazać np.: `Python 3.12.x`

---

### Krok 2 — Rozpakuj projekt

Rozpakuj plik `.zip` w dowolne miejsce, np.:
```
C:\Minikurs\
```

---

### Krok 3 — Otwórz terminal w folderze projektu

Wejdź do folderu `KURS` (tam gdzie jest plik `manage.py`), np.:
```
C:\Minikurs\KURS\
```

Kliknij prawym przyciskiem myszy w pustym miejscu folderu  
i wybierz **„Otwórz w terminalu"** lub **„Open in Terminal"**.

Albo otwórz `cmd` i wpisz:
```
cd C:\Minikurs\KURS
```

---

### Krok 4 — Utwórz wirtualne środowisko

```
python -m venv .venv
```

Poczekaj chwilę — zostanie utworzony folder `.venv`

---

### Krok 5 — Aktywuj wirtualne środowisko

```
.venv\Scripts\activate
```

Na początku linii pojawi się `(.venv)` — to znaczy że działa.

---

### Krok 6 — Zainstaluj wymagane biblioteki

```
pip install -r requirements.txt
```

Poczekaj aż wszystko się pobierze i zainstaluje.

---

### Krok 7 — Utwórz plik `.env`

W folderze `KURS` utwórz plik o nazwie `.env` (bez żadnego rozszerzenia)  
i wpisz do niego:
```
SECRET_KEY=lokalny-klucz-testowy-12345
DEBUG=True
```

> W Notatniku: Plik → Zapisz jako → Typ pliku: „Wszystkie pliki" → Nazwa: `.env`

---

### Krok 8 — Wykonaj migracje bazy danych

```
python manage.py migrate
```

Powinno pojawić się kilka linii z `OK`.

---

### Krok 9 — Załaduj dane (kursy, lekcje)

```
python manage.py loaddata minikurs/fixtures/dane.json
```

---

### Krok 10 — Utwórz konto administratora *(opcjonalnie)*

```
python manage.py createsuperuser
```

Podaj nazwę użytkownika, email i hasło.  
Panel admina dostępny pod: http://127.0.0.1:8000/admin/

---

### Krok 11 — Uruchom serwer

```
python manage.py runserver
```

Otwórz przeglądarkę i wejdź na: **http://127.0.0.1:8000/**

---

## ⏹️ Zatrzymanie serwera

W terminalu naciśnij: **Ctrl + C**

---

## 🔁 Kolejne uruchomienia

Po pierwszej instalacji wystarczy:

```
cd C:\Minikurs\KURS
.venv\Scripts\activate
python manage.py runserver
```

Następnie wejdź na: **http://127.0.0.1:8000/**

---

## 🗂️ Struktura projektu

```
Minikurs-HTML-CSS/
├── KURS/                   # główny folder Django
│   ├── manage.py
│   ├── requirements.txt
│   ├── kurs/               # konfiguracja projektu (settings.py, urls.py)
│   └── minikurs/           # aplikacja (modele, widoki, szablony)
│       └── fixtures/
│           └── dane.json   # dane początkowe (kursy, lekcje)
├── INSTRUKCJA.txt
├── URUCHOM.bat             # automatyczny instalator
└── python-installer.exe    # instalator Pythona 3.12
```

---

## ❓ Rozwiązywanie problemów

| Problem | Rozwiązanie |
|---|---|
| `python` nie jest rozpoznawany | Python nie jest w PATH — zainstaluj ponownie z zaznaczoną opcją **„Add Python to PATH"** |
| `No module named django` | Venv nie jest aktywny — uruchom `.venv\Scripts\activate` |
| Pusta strona z kursami | Pomiń krok 9 i dodaj dane ręcznie przez panel `/admin/` |
| Port 8000 zajęty | Uruchom na innym porcie: `python manage.py runserver 8080` |

---