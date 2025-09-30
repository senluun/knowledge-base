@echo off
chcp 65001 >nul
echo ========================================
echo УСТАНОВКА DJANGO И ЗАПУСК САЙТА
echo ========================================

echo 1. Удаляю старое виртуальное окружение:
if exist .venv rmdir /s /q .venv

echo 2. Создаю новое виртуальное окружение:
python -m venv .venv

echo 3. Активирую виртуальное окружение:
call .venv\Scripts\activate.bat

echo 4. Обновляю pip:
python -m pip install --upgrade pip

echo 5. Устанавливаю Django и зависимости:
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install django-widget-tweaks
pip install python-decouple

echo 6. Проверяю установку Django:
python -c "import django; print('Django version:', django.get_version())"

echo 7. Применяю миграции:
python manage.py migrate --noinput

echo 8. Создаю суперпользователя:
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin') | python manage.py shell

echo 9. Запускаю сервер:
echo ========================================
echo САЙТ ЗАПУЩЕН!
echo Откройте браузер: http://127.0.0.1:8000/knowledge/
echo Админка: http://127.0.0.1:8000/admin/ (admin/admin)
echo ========================================
python manage.py runserver 127.0.0.1:8000
