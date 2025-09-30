@echo off
chcp 65001 >nul
cd /d "%~dp0"

REM Откроет новое окно CMD, активирует .venv и запустит сервер
set "RUNLINE=call .venv\Scripts\activate.bat && set PYTHONUNBUFFERED=1 && set DJANGO_SETTINGS_MODULE=knowledge_base.settings && python manage.py runserver 127.0.0.1:8001"
start "Django Server :8001" cmd /k "%RUNLINE%"

echo Открылось новое окно с сервером. Если порт 8001 занят, запустите вручную:
echo   .venv\Scripts\activate.bat && python manage.py runserver 127.0.0.1:8002
pause


