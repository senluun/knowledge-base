@echo off
chcp 65001 >nul
echo ========================================
echo ПРОВЕРКА ПОРТОВ И ЗАПУСК НА ДРУГОМ ПОРТУ
echo ========================================

echo 1. Проверка порта 8001:
netstat -ano | find ":8001"
echo.

echo 2. Проверка порта 8000:
netstat -ano | find ":8000"
echo.

echo 3. Проверка порта 8080:
netstat -ano | find ":8080"
echo.

echo 4. Убиваю все процессы Python:
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul
echo.

echo 5. Активация .venv:
call .venv\Scripts\activate.bat
echo.

echo 6. Запуск на порту 8000:
echo ========================================
echo СЕРВЕР ЗАПУЩЕН НА ПОРТУ 8000!
echo Откройте браузер: http://127.0.0.1:8000/knowledge/
echo ========================================
python manage.py runserver 127.0.0.1:8000
