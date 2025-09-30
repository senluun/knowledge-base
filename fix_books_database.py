#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Исправление базы данных для библиотеки книг
Запустите этот файл двойным кликом для исправления ошибки
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from django.db import connection
from django.core.files.base import ContentFile
from django.utils.text import slugify

def create_tables():
    """Создание таблиц вручную"""
    print("Создание таблиц для библиотеки книг...")
    
    with connection.cursor() as cursor:
        # Создание таблицы books_category
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books_category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                slug VARCHAR(100) NOT NULL UNIQUE,
                description TEXT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Создание таблицы books_tag
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books_tag (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL UNIQUE,
                color VARCHAR(7) NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Создание таблицы books_book
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books_book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                slug VARCHAR(200) NOT NULL UNIQUE,
                author VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                cover_image VARCHAR(100),
                pdf_file VARCHAR(100) NOT NULL,
                is_published BOOLEAN NOT NULL DEFAULT 1,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                category_id INTEGER NOT NULL REFERENCES books_category(id)
            )
        """)
        
        # Создание таблицы books_book_tags
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books_book_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL REFERENCES books_book(id),
                tag_id INTEGER NOT NULL REFERENCES books_tag(id)
            )
        """)
        
        # Создание таблицы books_bookview
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books_bookview (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL REFERENCES books_book(id),
                user_id INTEGER REFERENCES accounts_user(id),
                ip_address CHAR(39),
                viewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Таблицы созданы успешно!")

def create_sample_data():
    """Создание тестовых данных"""
    print("Создание тестовых данных...")
    
    from books.models import Category, Tag, Book
    
    # Создание категорий
    categories_data = [
        {'name': 'Программирование', 'description': 'Книги по программированию и разработке ПО'},
        {'name': 'Дизайн', 'description': 'Книги по веб-дизайну и UI/UX'},
        {'name': 'Бизнес', 'description': 'Книги по бизнесу и менеджменту'},
    ]
    
    categories = []
    for cat_data in categories_data:
        try:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': slugify(cat_data['name'])
                }
            )
            categories.append(category)
            if created:
                print(f"✅ Создана категория: {category.name}")
            else:
                print(f"ℹ️ Категория уже существует: {category.name}")
        except Exception as e:
            print(f"⚠️ Ошибка создания категории {cat_data['name']}: {e}")
            # Попробуем найти существующую категорию
            try:
                category = Category.objects.get(name=cat_data['name'])
                categories.append(category)
                print(f"ℹ️ Найдена существующая категория: {category.name}")
            except Category.DoesNotExist:
                print(f"❌ Не удалось найти или создать категорию: {cat_data['name']}")
                continue
    
    # Создание тегов
    tags_data = [
        {'name': 'Python', 'color': '#3776ab'},
        {'name': 'JavaScript', 'color': '#f7df1e'},
        {'name': 'Django', 'color': '#092e20'},
        {'name': 'Бестселлер', 'color': '#ffd93d'},
        {'name': 'Новинка', 'color': '#6bcf7f'},
    ]
    
    tags = []
    for tag_data in tags_data:
        try:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'color': tag_data['color']}
            )
            tags.append(tag)
            if created:
                print(f"✅ Создан тег: {tag.name}")
            else:
                print(f"ℹ️ Тег уже существует: {tag.name}")
        except Exception as e:
            print(f"⚠️ Ошибка создания тега {tag_data['name']}: {e}")
            # Попробуем найти существующий тег
            try:
                tag = Tag.objects.get(name=tag_data['name'])
                tags.append(tag)
                print(f"ℹ️ Найден существующий тег: {tag.name}")
            except Tag.DoesNotExist:
                print(f"❌ Не удалось найти или создать тег: {tag_data['name']}")
                continue
    
    # Создание тестовых книг
    books_data = [
        {
            'title': 'Python для начинающих',
            'author': 'Марк Лутц',
            'description': 'Подробное руководство по изучению Python с нуля. Книга охватывает все основные концепции языка программирования Python.',
            'category': 'Программирование',
            'tags': ['Python', 'Бестселлер']
        },
        {
            'title': 'JavaScript: Подробное руководство',
            'author': 'Дэвид Флэнаган',
            'description': 'Исчерпывающее руководство по JavaScript для опытных программистов.',
            'category': 'Программирование',
            'tags': ['JavaScript', 'Бестселлер']
        },
        {
            'title': 'Django 4 в примерах',
            'author': 'Антонио Меле',
            'description': 'Практическое руководство по созданию веб-приложений с использованием Django 4.',
            'category': 'Программирование',
            'tags': ['Django', 'Python', 'Новинка']
        },
        {
            'title': 'Веб-дизайн для начинающих',
            'author': 'Джон Дакетт',
            'description': 'Полное руководство по HTML5 и CSS3 для создания современных веб-сайтов.',
            'category': 'Дизайн',
            'tags': ['Новинка']
        },
        {
            'title': 'Стартап. Настольная книга основателя',
            'author': 'Стив Бланк',
            'description': 'Практическое руководство по созданию успешного стартапа.',
            'category': 'Бизнес',
            'tags': ['Бестселлер']
        }
    ]
    
    # Создаем фиктивный PDF файл
    dummy_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
    
    for book_data in books_data:
        try:
            # Находим категорию
            category = next(cat for cat in categories if cat.name == book_data['category'])
            
            # Создаем книгу
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults={
                    'author': book_data['author'],
                    'description': book_data['description'],
                    'category': category,
                    'slug': slugify(book_data['title']),
                    'is_published': True
                }
            )
            
            if created:
                # Создаем фиктивный PDF файл
                pdf_file = ContentFile(dummy_pdf_content, name=f"{slugify(book_data['title'])}.pdf")
                book.pdf_file = pdf_file
                book.save()
                
                # Добавляем теги
                for tag_name in book_data['tags']:
                    tag = next(tag for tag in tags if tag.name == tag_name)
                    book.tags.add(tag)
                
                print(f"✅ Создана книга: {book.title}")
            else:
                print(f"ℹ️ Книга уже существует: {book.title}")
        except Exception as e:
            print(f"⚠️ Ошибка создания книги {book_data['title']}: {e}")
            continue
    
    print(f"\n📊 Статистика:")
    print(f"   Категорий: {Category.objects.count()}")
    print(f"   Тегов: {Tag.objects.count()}")
    print(f"   Книг: {Book.objects.count()}")

def main():
    """Основная функция"""
    print("=" * 60)
    print("🔧 ИСПРАВЛЕНИЕ БАЗЫ ДАННЫХ ДЛЯ БИБЛИОТЕКИ КНИГ")
    print("=" * 60)
    
    try:
        # Создание таблиц
        create_tables()
        
        # Создание тестовых данных
        create_sample_data()
        
        print("\n" + "=" * 60)
        print("✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!")
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
        sys.exit(1)

if __name__ == '__main__':
    main()
    input("\nНажмите Enter для выхода...")
