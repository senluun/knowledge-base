@echo off
setlocal
chcp 65001 >nul

REM Быстрый запуск Django без установки зависимостей и collectstatic

if not exist ".venv\Scripts\activate.bat" (
  echo .venv не найдено. Создаю...
  py -3 -m venv .venv || python -m venv .venv
)

call .venv\Scripts\activate.bat || (
  echo Не удалось активировать .venv
  pause
  exit /b 1
)

set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set DJANGO_SETTINGS_MODULE=knowledge_base.settings

echo Применяю миграции...
python manage.py migrate --noinput || goto :fail

echo Запуск сервера на http://127.0.0.1:8001
python manage.py runserver 127.0.0.1:8001
goto :eof

:fail
echo Ошибка при подготовке. См. сообщения выше.
pause


