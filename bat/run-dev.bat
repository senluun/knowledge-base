@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul

echo ========================================
echo      Django dev server launcher
echo ========================================
echo.

REM 1) Kill any process that occupies port 8001 (old runserver)
echo Проверка занятого порта 8001...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :8001 ^| findstr LISTENING') do (
    echo Найден процесс на порту 8001: PID=%%p
    taskkill /F /PID %%p >nul 2>&1
)

echo.
REM 2) Ensure venv exists
if not exist ".venv\Scripts\activate.bat" (
    echo Виртуальное окружение не найдено. Создаю .venv ...
    where py >nul 2>&1 && ( set _PY=py -3 ) || ( set _PY=python )
    %_PY% -m venv .venv || (
        echo ОШИБКА: Не удалось создать виртуальное окружение.
        pause
        exit /b 1
    )
)

REM 3) Activate venv
echo Активация виртуального окружения...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ОШИБКА: Не удалось активировать .venv
    pause
    exit /b 1
)

REM Настройка кодировки и подавление проблем pip в консоли
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set PIP_DISABLE_PIP_VERSION_CHECK=1
set RICH_NO_WINDOWS_CONSOLE=1

REM 4) Ensure pip and deps
echo Обновление pip и установка зависимостей (если требуется)...
python -m pip install --upgrade pip >nul 2>&1
if exist requirements.txt (
    python -m pip install -r requirements.txt --no-color || (
        echo ВНИМАНИЕ: Установка зависимостей завершилась с ошибками.
    )
)

REM 5) Django checks, migrate, collectstatic
echo.
echo Проверка настроек Django...
python manage.py check || (
    echo ОШИБКА: Django check не прошел.
    pause
    exit /b 1
)

echo Применение миграций...
python manage.py migrate --noinput || (
    echo ОШИБКА: migrate завершился с ошибкой.
    pause
    exit /b 1
)

echo Сбор статических файлов...
python manage.py collectstatic --noinput >nul

REM 6) Run server
echo.
echo Запуск сервера: http://127.0.0.1:8001
set DJANGO_SETTINGS_MODULE=knowledge_base.settings
python manage.py runserver 127.0.0.1:8001

echo.
echo Сервер остановлен.
pause


