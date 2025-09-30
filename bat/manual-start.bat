@echo off
chcp 65001 >nul
echo ========================================
echo РУЧНОЙ ЗАПУСК СЕРВЕРА
echo ========================================

echo 1. Активация .venv:
call .venv\Scripts\activate.bat

echo 2. Проверка настроек Django:
python -c "import django; print('Django version:', django.get_version())"
python -c "from django.conf import settings; print('DEBUG:', settings.DEBUG)"
python -c "from django.conf import settings; print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)"

echo 3. Попытка запуска на 0.0.0.0:8000:
echo ========================================
echo ЗАПУСКАЮ СЕРВЕР НА 0.0.0.0:8000
echo Откройте браузер: http://localhost:8000/knowledge/
echo ========================================
python manage.py runserver 0.0.0.0:8000

echo.
echo Сервер завершился с кодом: %ERRORLEVEL%
echo.
pause
