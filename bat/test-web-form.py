#!/usr/bin/env python
import requests
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from accounts.models import User
from knowledge.models import Category

def test_web_form():
    print("🌐 Тестирование веб-формы...")
    
    # Получаем пользователя и категорию
    user = User.objects.first()
    category = Category.objects.first()
    
    print(f"👤 Пользователь: {user.get_full_name()}")
    print(f"📁 Категория: {category.name} (ID: {category.id})")
    
    # Создаем сессию
    session = requests.Session()
    
    # Получаем страницу входа
    login_url = "http://127.0.0.1:8000/accounts/login/"
    response = session.get(login_url)
    print(f"📄 GET {login_url} - статус: {response.status_code}")
    
    if response.status_code != 200:
        print("❌ Не удалось загрузить страницу входа")
        return
    
    # Извлекаем CSRF токен
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    
    if not csrf_token:
        print("❌ CSRF токен не найден")
        return
    
    csrf_value = csrf_token['value']
    print(f"🔐 CSRF токен найден: {csrf_value[:20]}...")
    
    # Логинимся
    login_data = {
        'username': user.username,
        'password': 'admin123',  # Пароль по умолчанию
        'csrfmiddlewaretoken': csrf_value
    }
    
    response = session.post(login_url, data=login_data, allow_redirects=True)
    print(f"📤 POST {login_url} - статус: {response.status_code}")
    
    if response.status_code != 200:
        print("❌ Не удалось войти в систему")
        print(f"📄 Ответ: {response.text[:500]}...")
        return
    
    print("✅ Успешный вход в систему")
    
    # Получаем страницу создания статьи
    create_url = "http://127.0.0.1:8000/knowledge/create-article/"
    response = session.get(create_url)
    print(f"📄 GET {create_url} - статус: {response.status_code}")
    
    if response.status_code != 200:
        print("❌ Не удалось загрузить страницу создания статьи")
        return
    
    print("✅ Страница создания статьи загружена")
    
    # Извлекаем CSRF токен для формы создания статьи
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    
    if not csrf_token:
        print("❌ CSRF токен не найден на странице создания статьи")
        return
    
    csrf_value = csrf_token['value']
    print(f"🔐 CSRF токен для формы: {csrf_value[:20]}...")
    
    # Создаем данные для формы
    form_data = {
        'title': 'Тестовая статья через веб',
        'content': 'Это тестовая статья, созданная через веб-интерфейс.',
        'excerpt': 'Тестовое описание',
        'category': category.id,
        'tags': 'тест, веб',
        'is_featured': False,
        'allow_comments': True,
        'csrfmiddlewaretoken': csrf_value
    }
    
    print(f"📝 Данные формы: {form_data}")
    
    # Отправляем POST запрос
    response = session.post(create_url, data=form_data)
    print(f"📤 POST {create_url} - статус: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Редирект выполнен!")
        print(f"📍 Редирект на: {response.headers.get('Location', 'Не указан')}")
        
        # Проверяем, что статья создана
        from knowledge.models import Article
        article = Article.objects.filter(title='Тестовая статья через веб').first()
        if article:
            print(f"✅ Статья создана: {article.title} (статус: {article.status})")
            
            # Проверяем уведомления
            from moderation.models import Notification
            notifications = Notification.objects.filter(related_object_id=article.id)
            print(f"🔔 Создано уведомлений: {notifications.count()}")
            
            for notification in notifications:
                print(f"   - {notification.title} для {notification.user.get_full_name()}")
        else:
            print("❌ Статья не найдена в базе данных")
    else:
        print(f"❌ Ошибка отправки формы: {response.status_code}")
        print(f"📄 Ответ: {response.text[:500]}...")
        
        # Проверяем, есть ли ошибки в форме
        soup = BeautifulSoup(response.text, 'html.parser')
        error_divs = soup.find_all('div', class_='alert-danger')
        if error_divs:
            print("❌ Ошибки формы:")
            for error_div in error_divs:
                print(f"   {error_div.get_text().strip()}")
        
        # Проверяем, есть ли ошибки валидации
        error_lists = soup.find_all('ul', class_='errorlist')
        if error_lists:
            print("❌ Ошибки валидации:")
            for error_list in error_lists:
                print(f"   {error_list.get_text().strip()}")

if __name__ == "__main__":
    test_web_form()





import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from accounts.models import User
from knowledge.models import Category

def test_web_form():
    print("🌐 Тестирование веб-формы...")
    
    # Получаем пользователя и категорию
    user = User.objects.first()
    category = Category.objects.first()
    
    print(f"👤 Пользователь: {user.get_full_name()}")
    print(f"📁 Категория: {category.name} (ID: {category.id})")
    
    # Создаем сессию
    session = requests.Session()
    
    # Получаем страницу входа
    login_url = "http://127.0.0.1:8000/accounts/login/"
    response = session.get(login_url)
    print(f"📄 GET {login_url} - статус: {response.status_code}")
    
    if response.status_code != 200:
        print("❌ Не удалось загрузить страницу входа")
        return
    
    # Извлекаем CSRF токен
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    
    if not csrf_token:
        print("❌ CSRF токен не найден")
        return
    
    csrf_value = csrf_token['value']
    print(f"🔐 CSRF токен найден: {csrf_value[:20]}...")
    
    # Логинимся
    login_data = {
        'username': user.username,
        'password': 'admin123',  # Пароль по умолчанию
        'csrfmiddlewaretoken': csrf_value
    }
    
    response = session.post(login_url, data=login_data, allow_redirects=True)
    print(f"📤 POST {login_url} - статус: {response.status_code}")
    
    if response.status_code != 200:
        print("❌ Не удалось войти в систему")
        print(f"📄 Ответ: {response.text[:500]}...")
        return
    
    print("✅ Успешный вход в систему")
    
    # Получаем страницу создания статьи
    create_url = "http://127.0.0.1:8000/knowledge/create-article/"
    response = session.get(create_url)
    print(f"📄 GET {create_url} - статус: {response.status_code}")
    
    if response.status_code != 200:
        print("❌ Не удалось загрузить страницу создания статьи")
        return
    
    print("✅ Страница создания статьи загружена")
    
    # Извлекаем CSRF токен для формы создания статьи
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    
    if not csrf_token:
        print("❌ CSRF токен не найден на странице создания статьи")
        return
    
    csrf_value = csrf_token['value']
    print(f"🔐 CSRF токен для формы: {csrf_value[:20]}...")
    
    # Создаем данные для формы
    form_data = {
        'title': 'Тестовая статья через веб',
        'content': 'Это тестовая статья, созданная через веб-интерфейс.',
        'excerpt': 'Тестовое описание',
        'category': category.id,
        'tags': 'тест, веб',
        'is_featured': False,
        'allow_comments': True,
        'csrfmiddlewaretoken': csrf_value
    }
    
    print(f"📝 Данные формы: {form_data}")
    
    # Отправляем POST запрос
    response = session.post(create_url, data=form_data)
    print(f"📤 POST {create_url} - статус: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Редирект выполнен!")
        print(f"📍 Редирект на: {response.headers.get('Location', 'Не указан')}")
        
        # Проверяем, что статья создана
        from knowledge.models import Article
        article = Article.objects.filter(title='Тестовая статья через веб').first()
        if article:
            print(f"✅ Статья создана: {article.title} (статус: {article.status})")
            
            # Проверяем уведомления
            from moderation.models import Notification
            notifications = Notification.objects.filter(related_object_id=article.id)
            print(f"🔔 Создано уведомлений: {notifications.count()}")
            
            for notification in notifications:
                print(f"   - {notification.title} для {notification.user.get_full_name()}")
        else:
            print("❌ Статья не найдена в базе данных")
    else:
        print(f"❌ Ошибка отправки формы: {response.status_code}")
        print(f"📄 Ответ: {response.text[:500]}...")
        
        # Проверяем, есть ли ошибки в форме
        soup = BeautifulSoup(response.text, 'html.parser')
        error_divs = soup.find_all('div', class_='alert-danger')
        if error_divs:
            print("❌ Ошибки формы:")
            for error_div in error_divs:
                print(f"   {error_div.get_text().strip()}")
        
        # Проверяем, есть ли ошибки валидации
        error_lists = soup.find_all('ul', class_='errorlist')
        if error_lists:
            print("❌ Ошибки валидации:")
            for error_list in error_lists:
                print(f"   {error_list.get_text().strip()}")

if __name__ == "__main__":
    test_web_form()


















