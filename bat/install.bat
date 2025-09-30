@echo off
chcp 65001 >nul
echo ========================================
echo    Установка Базы знаний
echo ========================================
echo.

echo [1/8] Создание виртуального окружения...
python -m venv .venv
if errorlevel 1 (
    echo ОШИБКА: Не удалось создать виртуальное окружение
    echo Убедитесь, что Python установлен
    pause
    exit /b 1
)

echo [2/8] Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo [3/8] Установка зависимостей...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА: Не удалось установить зависимости
    pause
    exit /b 1
)

echo [4/8] Создание необходимых директорий...
if not exist "static" mkdir static
if not exist "media" mkdir media  
if not exist "logs" mkdir logs
echo Директории созданы

echo [5/8] Проверка Django...
python -c "import django; print('Django версия:', django.get_version())"
if errorlevel 1 (
    echo ОШИБКА: Django не установлен корректно
    pause
    exit /b 1
)

echo [6/8] Проверка Django...
python manage.py check
if errorlevel 1 (
    echo ОШИБКА: Проблемы с настройками Django
    pause
    exit /b 1
)

echo [7/8] Создание и применение миграций...
python manage.py makemigrations
if errorlevel 1 (
    echo ОШИБКА: Не удалось создать миграции
    echo Проверьте модели на ошибки
    pause
    exit /b 1
)

python manage.py migrate
if errorlevel 1 (
    echo ОШИБКА: Не удалось применить миграции
    pause
    exit /b 1
)

echo [8/8] Создание суперпользователя и инициализация...
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='Администратор',
        last_name='Системы'
    )
    print('Суперпользователь создан: admin/admin123')
else:
    print('Суперпользователь уже существует')
EOF

python manage.py init_project

echo.
echo ========================================
echo    Установка завершена успешно!
echo ========================================
echo.
echo 🎉 База знаний готова к работе!
echo.
echo 📋 Доступ к системе:
echo   URL: http://localhost:8000
echo   Админ панель: http://localhost:8000/admin
echo   Логин: admin
echo   Пароль: admin123
echo.
echo 🚀 Для запуска сервера:
echo   start.bat
echo.
pause
















