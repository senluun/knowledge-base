@echo off
chcp 65001 >nul
echo ========================================
echo ТЕСТИРОВАНИЕ СЕРВЕРА
echo ========================================

echo 1. Активация .venv:
call .venv\Scripts\activate.bat
echo.

echo 2. Проверка Django:
python manage.py check
echo.

echo 3. Запуск сервера с максимальным выводом:
echo ========================================
echo СЕРВЕР ЗАПУЩАЕТСЯ...
echo Если увидите ошибку - пришлите её мне
echo ========================================
python manage.py runserver 127.0.0.1:8000 --verbosity=3 --traceback
echo.
echo Сервер завершился!
echo Код выхода: %ERRORLEVEL%
echo.
pause
