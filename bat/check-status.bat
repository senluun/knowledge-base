@echo off
chcp 65001 >nul
echo ========================================
echo ДИАГНОСТИКА САЙТА
echo ========================================

echo 1. Проверка процессов Python:
tasklist | findstr python
echo.

echo 2. Проверка порта 8001:
netstat -ano | find ":8001"
echo.

echo 3. Проверка доступности сайта:
curl -I http://127.0.0.1:8001/ 2>nul
if errorlevel 1 (
    echo Сайт недоступен!
) else (
    echo Сайт доступен!
)
echo.

echo 4. Проверка Django:
call .venv\Scripts\activate.bat
python manage.py check
echo.

echo 5. Попытка запуска сервера в тестовом режиме:
python manage.py runserver 127.0.0.1:8001 --noreload
pause
