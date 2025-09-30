@echo off
chcp 65001 >nul
echo ========================================
echo ПОИСК НАСТОЯЩЕЙ ОШИБКИ
echo ========================================

echo 1. Активация .venv:
call .venv\Scripts\activate.bat

echo 2. Проверка Python:
python --version

echo 3. Проверка Django:
python -c "import django; print('Django OK')"

echo 4. Проверка настроек:
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings'); import django; django.setup(); print('Settings OK')"

echo 5. Проверка базы данных:
python manage.py check --database default

echo 6. Попытка запуска с выводом ошибок:
echo ========================================
echo ЗАПУСКАЮ СЕРВЕР (все ошибки будут показаны)
echo ========================================
python manage.py runserver 127.0.0.1:5000 2>&1

echo.
echo ========================================
echo СЕРВЕР ЗАВЕРШИЛСЯ!
echo ========================================
pause
