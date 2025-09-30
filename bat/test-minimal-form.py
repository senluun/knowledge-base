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
from bs4 import BeautifulSoup

def test_minimal_form():
    print("🧪 Тест минимальной формы...")
    
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
    
    # Извлекаем CSRF токен
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    csrf_value = csrf_token['value']
    
    # Логинимся
    login_data = {
        'username': user.username,
        'password': 'admin123',
        'csrfmiddlewaretoken': csrf_value
    }
    
    session.post(login_url, data=login_data, allow_redirects=True)
    
    # Получаем страницу создания статьи
    create_url = "http://127.0.0.1:8000/knowledge/create-article/"
    response = session.get(create_url)
    
    # Извлекаем CSRF токен для формы создания статьи
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    csrf_value = csrf_token['value']
    
    # Тест 1: Минимальные данные
    print("\n📝 Тест 1: Минимальные данные")
    form_data = {
        'title': 'Минимальная статья тест 2',
        'content': 'Содержание статьи',
        'category': category.id,
        'csrfmiddlewaretoken': csrf_value
    }
    
    response = session.post(create_url, data=form_data)
    print(f"📤 POST статус: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Редирект выполнен!")
    else:
        print("❌ Ошибка отправки формы")
        soup = BeautifulSoup(response.text, 'html.parser')
        error_divs = soup.find_all('div', class_='alert-danger')
        if error_divs:
            print("❌ Ошибки формы:")
            for error_div in error_divs:
                print(f"   {error_div.get_text().strip()}")
    
    # Тест 2: Полные данные
    print("\n📝 Тест 2: Полные данные")
    form_data = {
        'title': 'Полная статья тест 2',
        'content': 'Это полное содержание статьи с подробным описанием.',
        'excerpt': 'Краткое описание статьи',
        'category': category.id,
        'tags': 'тест, статья',
        'is_featured': False,
        'allow_comments': True,
        'csrfmiddlewaretoken': csrf_value
    }
    
    response = session.post(create_url, data=form_data)
    print(f"📤 POST статус: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Редирект выполнен!")
    else:
        print("❌ Ошибка отправки формы")
        soup = BeautifulSoup(response.text, 'html.parser')
        error_divs = soup.find_all('div', class_='alert-danger')
        if error_divs:
            print("❌ Ошибки формы:")
            for error_div in error_divs:
                print(f"   {error_div.get_text().strip()}")

if __name__ == "__main__":
    test_minimal_form()





import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from accounts.models import User
from knowledge.models import Category
from bs4 import BeautifulSoup

def test_minimal_form():
    print("🧪 Тест минимальной формы...")
    
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
    
    # Извлекаем CSRF токен
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    csrf_value = csrf_token['value']
    
    # Логинимся
    login_data = {
        'username': user.username,
        'password': 'admin123',
        'csrfmiddlewaretoken': csrf_value
    }
    
    session.post(login_url, data=login_data, allow_redirects=True)
    
    # Получаем страницу создания статьи
    create_url = "http://127.0.0.1:8000/knowledge/create-article/"
    response = session.get(create_url)
    
    # Извлекаем CSRF токен для формы создания статьи
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    csrf_value = csrf_token['value']
    
    # Тест 1: Минимальные данные
    print("\n📝 Тест 1: Минимальные данные")
    form_data = {
        'title': 'Минимальная статья тест 2',
        'content': 'Содержание статьи',
        'category': category.id,
        'csrfmiddlewaretoken': csrf_value
    }
    
    response = session.post(create_url, data=form_data)
    print(f"📤 POST статус: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Редирект выполнен!")
    else:
        print("❌ Ошибка отправки формы")
        soup = BeautifulSoup(response.text, 'html.parser')
        error_divs = soup.find_all('div', class_='alert-danger')
        if error_divs:
            print("❌ Ошибки формы:")
            for error_div in error_divs:
                print(f"   {error_div.get_text().strip()}")
    
    # Тест 2: Полные данные
    print("\n📝 Тест 2: Полные данные")
    form_data = {
        'title': 'Полная статья тест 2',
        'content': 'Это полное содержание статьи с подробным описанием.',
        'excerpt': 'Краткое описание статьи',
        'category': category.id,
        'tags': 'тест, статья',
        'is_featured': False,
        'allow_comments': True,
        'csrfmiddlewaretoken': csrf_value
    }
    
    response = session.post(create_url, data=form_data)
    print(f"📤 POST статус: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Редирект выполнен!")
    else:
        print("❌ Ошибка отправки формы")
        soup = BeautifulSoup(response.text, 'html.parser')
        error_divs = soup.find_all('div', class_='alert-danger')
        if error_divs:
            print("❌ Ошибки формы:")
            for error_div in error_divs:
                print(f"   {error_div.get_text().strip()}")

if __name__ == "__main__":
    test_minimal_form()


















