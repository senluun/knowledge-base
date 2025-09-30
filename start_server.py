#!/usr/bin/env python
"""
Скрипт для запуска Django сервера
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("=" * 50)
    print("ЗАПУСК САЙТА БАЗЫ ЗНАНИЙ")
    print("=" * 50)
    
    # Проверяем Python
    print(f"Python версия: {sys.version}")
    
    # Проверяем Django
    try:
        import django
        from django.core.management import execute_from_command_line
        print(f"Django версия: {django.get_version()}")
    except ImportError:
        print("ОШИБКА: Django не установлен!")
        print("Установите зависимости: pip install -r requirements.txt")
        return 1
    
    # Устанавливаем настройки Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
    
    try:
        # Проверяем настройки
        print("Проверка настроек Django...")
        execute_from_command_line(['manage.py', 'check'])
        print("✓ Настройки Django корректны")
        
        # Применяем миграции
        print("Применение миграций...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✓ Миграции применены")
        
        # Запускаем сервер
        print("=" * 50)
        print("ВСЕ ГОТОВО! Откройте браузер:")
        print("http://127.0.0.1:8001/knowledge/")
        print("=" * 50)
        print("Запуск сервера...")
        
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8001'])
        
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
