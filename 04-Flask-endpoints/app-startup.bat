@echo off
REM Tworzenie środowiska wirtualnego
if not exist venv (
    python -m venv venv
)

REM Aktywowanie środowiska wirtualnego
call venv\Scripts\activate

REM Instalowanie wymaganych paczek
pip install Flask
pip install flask-sqlalchemy
pip install requests
pip install pyshark

REM Uruchamianie aplikacji Flask w oddzielnych terminalach
start cmd /k "call venv\Scripts\activate && python app.py"
start cmd /k "call venv\Scripts\activate && python test.py"
start cmd /k "call venv\Scripts\activate && python display_pcap.py"

REM Zakończenie
echo Wszystkie aplikacje uruchomione w oddzielnych terminalach! Wciśnij dowolny klawisz, aby zamknąć...
pause
