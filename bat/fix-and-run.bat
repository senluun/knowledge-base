@echo off
chcp 65001 >nul
echo ========================================
echo ИСПРАВЛЕНИЕ И ЗАПУСК САЙТА
echo ========================================

echo 1. Убиваю все процессы Python...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo 2. Убиваю процессы на порту 8001...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8001"') do taskkill /f /pid %%a 2>nul

echo 3. Создаю виртуальное окружение...
if exist .venv rmdir /s /q .venv
python -m venv .venv

echo 4. Активирую окружение...
call .venv\Scripts\activate.bat

echo 5. Устанавливаю зависимости...
pip install --upgrade pip
pip install -r requirements.txt

echo 6. Применяю миграции...
python manage.py migrate --noinput

echo 7. Создаю суперпользователя (если нужно)...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin') | python manage.py shell

echo 8. Запускаю сервер...
echo ========================================
echo СЕРВЕР ЗАПУЩЕН! Откройте браузер:
echo http://127.0.0.1:8001/knowledge/
echo ========================================
python manage.py runserver 127.0.0.1:8001
