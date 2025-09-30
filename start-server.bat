@echo off
echo ========================================
echo    Запуск Django сервера
echo ========================================
echo.

REM Активация виртуального окружения
if exist ".venv\Scripts\activate.bat" (
    echo Активация виртуального окружения...
    call .venv\Scripts\activate.bat
) else (
    echo ОШИБКА: Виртуальное окружение не найдено!
    echo Создайте его командой: python -m venv .venv
    pause
    exit /b 1
)

echo.
echo Проверка миграций...
python manage.py migrate --noinput

echo.
echo Сбор статических файлов...
python manage.py collectstatic --noinput

echo.
echo Запуск сервера на http://127.0.0.1:8001
echo Для остановки нажмите Ctrl+C
echo.

python manage.py runserver 127.0.0.1:8001

pause

