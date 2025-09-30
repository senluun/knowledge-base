@echo off
chcp 65001 >nul
echo ========================================
echo ПРИНУДИТЕЛЬНЫЙ ЗАПУСК САЙТА
echo ========================================

echo 1. Убиваю все процессы...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo 2. Очищаю порт 8001...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8001"') do taskkill /f /pid %%a 2>nul

echo 3. Проверяю Python...
python --version
if errorlevel 1 (
    echo ОШИБКА: Python не найден!
    pause
    exit /b 1
)

echo 4. Пересоздаю виртуальное окружение...
if exist .venv rmdir /s /q .venv
python -m venv .venv

echo 5. Активирую окружение...
call .venv\Scripts\activate.bat

echo 6. Устанавливаю зависимости...
pip install -r requirements.txt

echo 7. Проверяю Django...
python manage.py check
if errorlevel 1 (
    echo ОШИБКА: Django check failed!
    echo Содержимое ошибки:
    python manage.py check --verbosity=2
    pause
    exit /b 1
)

echo 8. Применяю миграции...
python manage.py migrate --noinput

echo 9. Запускаю сервер...
echo ========================================
echo СЕРВЕР ЗАПУЩАЕТСЯ...
echo Откройте браузер: http://127.0.0.1:8001/knowledge/
echo ========================================
python manage.py runserver 127.0.0.1:8001 --verbosity=2
