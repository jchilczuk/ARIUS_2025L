@echo off
REM Tworzenie środowiska wirtualnego
python -m venv venv

REM Aktywowanie środowiska wirtualnego
call venv\Scripts\activate

REM Instalowanie wymaganych paczek
pip install Flask
pip install flask-sqlalchemy

REM Uruchamianie aplikacji Flask
python app.py

REM Zakończenie
echo Aplikacja uruchomiona! Wciśnij dowolny klawisz, aby zamknąć...
pause
