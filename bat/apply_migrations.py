#!/usr/bin/env python
"""
Скрипт для применения миграций приложения books
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from django.core.management import execute_from_command_line

def apply_migrations():
    """Применение миграций для приложения books"""
    print("Применение миграций для приложения books...")
    
    try:
        # Создание миграций
        print("Создание миграций...")
        execute_from_command_line(['manage.py', 'makemigrations', 'books'])
        
        # Применение миграций
        print("Применение миграций...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("Миграции успешно применены!")
        
    except Exception as e:
        print(f"Ошибка при применении миграций: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = apply_migrations()
    if success:
        print("\n✅ Миграции применены успешно!")
        print("Теперь вы можете перейти на http://127.0.0.1:8001/books/")
    else:
        print("\n❌ Ошибка при применении миграций")
        sys.exit(1)

