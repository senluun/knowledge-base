@echo off
chcp 65001 >nul
echo ========================================
echo ПРОСТОЙ РАБОЧИЙ ЗАПУСК
echo ========================================

echo 1. Убиваю ВСЕ процессы Python:
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo 2. Очищаю ВСЕ порты:
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000"') do taskkill /f /pid %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8001"') do taskkill /f /pid %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8080"') do taskkill /f /pid %%a 2>nul

echo 3. Активирую .venv:
call .venv\Scripts\activate.bat

echo 4. Запускаю на порту 3000 (редко занят):
echo ========================================
echo САЙТ ЗАПУЩЕН НА ПОРТУ 3000!
echo ОТКРОЙТЕ БРАУЗЕР: http://127.0.0.1:3000/
echo ========================================
python manage.py runserver 127.0.0.1:3000
