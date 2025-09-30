@echo off
chcp 65001 >nul
echo ========================================
echo РУЧНАЯ ОТЛАДКА
echo ========================================

echo 1. Активация .venv:
call .venv\Scripts\activate.bat

echo 2. Проверка файлов проекта:
dir manage.py
dir knowledge_base
dir knowledge
dir accounts
dir moderation

echo 3. Попытка запуска с --noreload:
echo ========================================
echo ЗАПУСКАЮ С --noreload
echo ========================================
python manage.py runserver 127.0.0.1:5000 --noreload

echo.
echo ========================================
echo СЕРВЕР ЗАВЕРШИЛСЯ!
echo ========================================
pause
