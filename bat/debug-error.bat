@echo off
chcp 65001 >nul
echo ========================================
echo ОТЛАДКА ОШИБОК DJANGO
echo ========================================

echo 1. Проверка Python...
python --version
echo.

echo 2. Создание .venv...
if exist .venv rmdir /s /q .venv
python -m venv .venv
echo.

echo 3. Активация .venv...
call .venv\Scripts\activate.bat
echo.

echo 4. Установка зависимостей...
pip install -r requirements.txt
echo.

echo 5. ПРОВЕРКА DJANGO (здесь может быть ошибка)...
python manage.py check --verbosity=2
echo.
echo Код выхода Django check: %ERRORLEVEL%
echo.

echo 6. Попытка миграций...
python manage.py migrate --noinput
echo.
echo Код выхода миграций: %ERRORLEVEL%
echo.

echo 7. Попытка запуска сервера...
echo ========================================
echo ЗАПУСКАЮ СЕРВЕР (если есть ошибка - увидите ниже)
echo ========================================
python manage.py runserver 127.0.0.1:8001 --verbosity=2
echo.
echo Сервер завершился с кодом: %ERRORLEVEL%
echo.

echo ========================================
echo ДИАГНОСТИКА ЗАВЕРШЕНА
echo ========================================
pause
