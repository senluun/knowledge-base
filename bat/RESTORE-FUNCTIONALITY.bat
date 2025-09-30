@echo off
chcp 65001 >nul
echo ========================================
echo ВОССТАНОВЛЕНИЕ ФУНКЦИОНАЛА
echo ========================================

echo 1. Активация .venv:
call .venv\Scripts\activate.bat

echo 2. Создание миграций:
python manage.py makemigrations

echo 3. Применение миграций:
python manage.py migrate --noinput

echo 4. Создание суперпользователя:
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin') | python manage.py shell

echo 5. Создание тестовых данных:
python manage.py shell -c "
from knowledge.models import Category, Article
from accounts.models import User

# Создаем категории
if not Category.objects.exists():
    categories = [
        {'name': 'Программирование', 'description': 'Статьи по программированию', 'icon': 'fas fa-code', 'color': '#007bff'},
        {'name': 'Дизайн', 'description': 'Статьи по дизайну', 'icon': 'fas fa-paint-brush', 'color': '#28a745'},
        {'name': 'Маркетинг', 'description': 'Статьи по маркетингу', 'icon': 'fas fa-chart-line', 'color': '#ffc107'},
        {'name': 'Управление', 'description': 'Статьи по управлению', 'icon': 'fas fa-users', 'color': '#dc3545'},
    ]
    
    for cat_data in categories:
        Category.objects.create(**cat_data)
    print('Категории созданы')

# Создаем тестовые статьи
if not Article.objects.exists():
    admin_user = User.objects.get(username='admin')
    programming_cat = Category.objects.get(name='Программирование')
    
    articles = [
        {
            'title': 'Введение в Python',
            'content': 'Python - это высокоуровневый язык программирования...',
            'category': programming_cat,
            'author': admin_user,
            'status': 'published',
            'is_featured': True
        },
        {
            'title': 'Основы Django',
            'content': 'Django - это веб-фреймворк для Python...',
            'category': programming_cat,
            'author': admin_user,
            'status': 'published',
            'is_featured': True
        },
        {
            'title': 'Принципы дизайна',
            'content': 'Хороший дизайн основывается на принципах...',
            'category': Category.objects.get(name='Дизайн'),
            'author': admin_user,
            'status': 'published',
            'is_featured': False
        }
    ]
    
    for article_data in articles:
        Article.objects.create(**article_data)
    print('Статьи созданы')

print('Тестовые данные созданы!')
"

echo 6. Сбор статических файлов:
python manage.py collectstatic --noinput

echo 7. Запуск сервера:
echo ========================================
echo САЙТ ВОССТАНОВЛЕН!
echo Откройте браузер: http://127.0.0.1:8000/knowledge/
echo Админка: http://127.0.0.1:8000/admin/ (admin/admin)
echo ========================================
python manage.py runserver 127.0.0.1:8000
