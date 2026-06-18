@echo off
chcp 65001 >nul
title Minikurs HTML/CSS — Instalator

echo.
echo ================================================================
echo   MINIKURS HTML/CSS — AUTOMATYCZNA INSTALACJA
echo ================================================================
echo.

:: Wejdz do folderu KURS gdzie jest manage.py
cd /d "%~dp0KURS"

if not exist "manage.py" (
    echo [BLAD] Nie znaleziono pliku manage.py w folderze KURS
    pause
    exit /b 1
)

echo [1/7] Sprawdzam Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [!] Python nie jest zainstalowany lub nie jest w PATH.
    echo.
    echo Pobierz Python ze strony: https://www.python.org/downloads/
    echo WAZNE: Zaznacz "Add Python to PATH" podczas instalacji!
    echo.
    echo Po zainstalowaniu Pythona uruchom ten plik ponownie.
    pause
    exit /b 1
)
python --version
echo     OK

echo.
echo [2/7] Tworze wirtualne srodowisko (.venv)...
if exist ".venv" (
    echo     Juz istnieje — pomijam.
) else (
    python -m venv .venv
    echo     OK
)

echo.
echo [3/7] Aktywuje wirtualne srodowisko...
call .venv\Scripts\activate.bat
echo     OK

echo.
echo [4/7] Instaluje wymagane biblioteki (moze chwile potrwac)...
pip install -r requirements.txt --quiet
echo     OK

echo.
echo [5/7] Sprawdzam plik .env...
if exist ".env" (
    echo     Juz istnieje — pomijam.
) else (
    echo SECRET_KEY=lokalny-klucz-testowy-12345> .env
    echo DEBUG=True>> .env
    echo     Utworzono plik .env
)

echo.
echo [6/7] Wykonuje migracje bazy danych...
python manage.py migrate
echo     OK

echo.
echo [7/7] Laduje dane poczatkowe...
if exist "minikurs\fixtures\dane.json" (
    python manage.py loaddata minikurs/fixtures/dane.json
    echo     OK
) else (
    echo     Brak pliku dane.json — pomijam.
)

echo.
echo ================================================================
echo   Instalacja zakonczona! Uruchamiam serwer...
echo   Otworz przegladarke i wejdz na: http://127.0.0.1:8000/
echo   Aby zatrzymac serwer nacisnij: Ctrl + C
echo ================================================================
echo.
python manage.py runserver
