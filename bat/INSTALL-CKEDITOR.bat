@echo off
chcp 65001 >nul
echo ========================================
echo УСТАНОВКА CKEDITOR И ЗАПУСК
echo ========================================

echo 1. Активация .venv:
call .venv\Scripts\activate.bat

echo 2. Установка CKEditor:
pip install django-ckeditor

echo 3. Установка дополнительных зависимостей:
pip install Pillow

echo 4. Создание миграций:
python manage.py makemigrations

echo 5. Применение миграций:
python manage.py migrate --noinput

echo 6. Создание суперпользователя:
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin') | python manage.py shell

echo 7. Запуск сервера:
echo ========================================
echo САЙТ ЗАПУЩЕН!
echo Откройте браузер: http://127.0.0.1:8000/knowledge/
echo Админка: http://127.0.0.1:8000/admin/ (admin/admin)
echo ========================================
python manage.py runserver 127.0.0.1:8000
