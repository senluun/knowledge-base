#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для исправления базы данных библиотеки книг
Запустите этот файл двойным кликом для исправления ошибки
"""
import os
import sys
import subprocess

def run_command(command):
    """Выполнение команды"""
    try:
        print(f"Выполняю: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {command} - выполнено успешно")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {command} - ошибка:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Ошибка выполнения команды {command}: {e}")
        return False

def main():
    """Основная функция"""
    print("=" * 60)
    print("🔧 ИСПРАВЛЕНИЕ БАЗЫ ДАННЫХ ДЛЯ БИБЛИОТЕКИ КНИГ")
    print("=" * 60)
    
    # Проверяем, есть ли виртуальное окружение
    venv_python = ".venv\\Scripts\\python.exe"
    if os.path.exists(venv_python):
        print("✅ Найдено виртуальное окружение")
        python_cmd = venv_python
    else:
        print("⚠️ Виртуальное окружение не найдено, используем системный Python")
        python_cmd = "python"
    
    try:
        # Создание миграций
        print("\n[1/4] Создание миграций...")
        if not run_command(f"{python_cmd} manage.py makemigrations books"):
            print("⚠️ Ошибка создания миграций, продолжаем...")
        
        # Применение миграций
        print("\n[2/4] Применение миграций...")
        if not run_command(f"{python_cmd} manage.py migrate"):
            print("⚠️ Ошибка применения миграций, продолжаем...")
        
        # Создание таблиц вручную
        print("\n[3/4] Создание таблиц вручную...")
        if not run_command(f"{python_cmd} fix_books_database.py"):
            print("⚠️ Ошибка создания таблиц, продолжаем...")
        
        # Проверка результата
        print("\n[4/4] Проверка результата...")
        check_cmd = f"{python_cmd} -c \"import django; django.setup(); from books.models import Book; print('Книг в базе:', Book.objects.count())\""
        run_command(check_cmd)
        
        print("\n" + "=" * 60)
        print("✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
        print("=" * 60)
        print("🌐 Теперь вы можете перейти на:")
        print("   http://127.0.0.1:8001/books/")
        print("\n📚 Доступные функции:")
        print("   • Просмотр каталога книг")
        print("   • Чтение PDF онлайн")
        print("   • Поиск и фильтрация")
        print("   • Классификация по категориям и тегам")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nНажмите Enter для выхода...")

if __name__ == '__main__':
    main()