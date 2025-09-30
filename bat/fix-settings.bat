@echo off
chcp 65001 >nul
echo ========================================
echo ИСПРАВЛЕНИЕ НАСТРОЕК И ЗАПУСК
echo ========================================

echo 1. Активация виртуального окружения:
call .venv\Scripts\activate.bat

echo 2. Установка переменной окружения:
set DJANGO_SETTINGS_MODULE=knowledge_base.settings

echo 3. Проверка Django с правильными настройками:
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings'); import django; django.setup(); from django.conf import settings; print('DEBUG:', settings.DEBUG); print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)"

echo 4. Применяю миграции:
python manage.py migrate --noinput

echo 5. Создаю суперпользователя:
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin') | python manage.py shell

echo 6. Запускаю сервер:
echo ========================================
echo САЙТ ЗАПУЩЕН!
echo Откройте браузер: http://127.0.0.1:8000/knowledge/
echo Админка: http://127.0.0.1:8000/admin/ (admin/admin)
echo ========================================
python manage.py runserver 127.0.0.1:8000
