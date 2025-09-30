@echo off
chcp 65001 >nul
echo ========================================
echo ПОКАЗАТЬ ОШИБКУ DJANGO
echo ========================================

echo 1. Активация .venv:
call .venv\Scripts\activate.bat

echo 2. Проверка Django с подробным выводом:
python manage.py check --verbosity=3

echo 3. Попытка запуска с максимальным выводом:
echo ========================================
echo ЗАПУСКАЮ СЕРВЕР (если есть ошибка - увидите ниже)
echo ========================================
python manage.py runserver 127.0.0.1:3000 --verbosity=3 --traceback

echo.
echo ========================================
echo СЕРВЕР ЗАВЕРШИЛСЯ!
echo Код выхода: %ERRORLEVEL%
echo ========================================
pause
