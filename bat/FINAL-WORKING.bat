@echo off
chcp 65001 >nul
echo ========================================
echo ФИНАЛЬНЫЙ РАБОЧИЙ ЗАПУСК
echo ========================================

echo 1. Активация .venv:
call .venv\Scripts\activate.bat

echo 2. Проверка Django:
python manage.py check

echo 3. Запуск сервера:
echo ========================================
echo САЙТ ЗАПУЩЕН!
echo Откройте браузер: http://127.0.0.1:8000/knowledge/
echo Админка: http://127.0.0.1:8000/admin/ (admin/admin)
echo ========================================
python manage.py runserver 127.0.0.1:8000
