@echo off
chcp 65001 >nul
echo ========================================
echo ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ
echo ========================================

echo 1. Активация .venv:
call .venv\Scripts\activate.bat

echo 2. Создание миграций:
python manage.py makemigrations

echo 3. Применение миграций:
python manage.py migrate --noinput

echo 4. Создание суперпользователя:
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin') | python manage.py shell

echo 5. Запуск сервера:
echo ========================================
echo САЙТ ЗАПУЩЕН!
echo Откройте браузер: http://127.0.0.1:8000/knowledge/
echo Админка: http://127.0.0.1:8000/admin/ (admin/admin)
echo ========================================
python manage.py runserver 127.0.0.1:8000
