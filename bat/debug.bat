@echo off
chcp 65001 >nul
echo === Диагностика Django ===

echo 1. Проверка Python...
python --version
if errorlevel 1 (
    echo Python не найден!
    pause
    exit /b 1
)

echo 2. Активация виртуального окружения...
if not exist ".venv\Scripts\activate.bat" (
    echo .venv не найдено!
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat

echo 3. Проверка Django...
python manage.py check
if errorlevel 1 (
    echo Django check failed!
    pause
    exit /b 1
)

echo 4. Запуск сервера с подробным выводом...
python manage.py runserver 127.0.0.1:8001 --verbosity=2
pause
