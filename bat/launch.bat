@echo off
chcp 65001 >nul
echo ========================================
echo ЗАПУСК САЙТА БАЗЫ ЗНАНИЙ
echo ========================================

echo Проверка Python...
python --version
if errorlevel 1 (
    echo ОШИБКА: Python не найден!
    echo Установите Python с https://python.org
    pause
    exit /b 1
)

echo Создание виртуального окружения...
if not exist .venv (
    python -m venv .venv
    if errorlevel 1 (
        echo ОШИБКА: Не удалось создать .venv
        pause
        exit /b 1
    )
)

echo Активация окружения...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ОШИБКА: Не удалось активировать .venv
    pause
    exit /b 1
)

echo Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА: Не удалось установить зависимости
    pause
    exit /b 1
)

echo Проверка Django...
python manage.py check
if errorlevel 1 (
    echo ОШИБКА: Django check failed!
    pause
    exit /b 1
)

echo Применение миграций...
python manage.py migrate --noinput
if errorlevel 1 (
    echo ОШИБКА: Миграции не применились
    pause
    exit /b 1
)

echo ========================================
echo ВСЕ ГОТОВО! Откройте браузер:
echo http://127.0.0.1:8001/knowledge/
echo ========================================
echo Запуск сервера...
python manage.py runserver 127.0.0.1:8001
pause
