@echo off
chcp 65001 >nul
echo ========================================
echo ЗАПУСК САЙТА БАЗЫ ЗНАНИЙ
echo ========================================

echo Шаг 1: Проверка Python
python --version
if errorlevel 1 (
    echo ОШИБКА: Python не установлен!
    pause
    exit /b 1
)

echo Шаг 2: Создание виртуального окружения
if not exist .venv (
    echo Создаю виртуальное окружение...
    python -m venv .venv
    if errorlevel 1 (
        echo ОШИБКА: Не удалось создать .venv
        pause
        exit /b 1
    )
)

echo Шаг 3: Активация окружения
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ОШИБКА: Не удалось активировать .venv
    pause
    exit /b 1
)

echo Шаг 4: Установка зависимостей
pip install -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА: Не удалось установить зависимости
    pause
    exit /b 1
)

echo Шаг 5: Проверка Django
python manage.py check
if errorlevel 1 (
    echo ОШИБКА: Django check failed!
    echo Детали ошибки:
    python manage.py check --verbosity=2
    pause
    exit /b 1
)

echo Шаг 6: Применение миграций
python manage.py migrate --noinput
if errorlevel 1 (
    echo ОШИБКА: Миграции не применились
    pause
    exit /b 1
)

echo Шаг 7: Запуск сервера
echo ========================================
echo ВСЕ ГОТОВО! Откройте браузер:
echo http://127.0.0.1:8001/knowledge/
echo ========================================
python manage.py runserver 127.0.0.1:8001
