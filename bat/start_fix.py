#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для исправления базы данных библиотеки книг
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
    print("Creating tables for books library...")
    
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
        
        print("Tables created successfully!")

def create_sample_data():
    """Создание тестовых данных"""
    print("Creating sample data...")
    
    from books.models import Category, Tag, Book
    
    # Создание категорий
    categories_data = [
        {'name': 'Programming', 'description': 'Books about programming and software development'},
        {'name': 'Design', 'description': 'Books about web design and UI/UX'},
        {'name': 'Business', 'description': 'Books about business and management'},
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
                print(f"Created category: {category.name}")
            else:
                print(f"Category already exists: {category.name}")
        except Exception as e:
            print(f"Error creating category {cat_data['name']}: {e}")
            try:
                category = Category.objects.get(name=cat_data['name'])
                categories.append(category)
                print(f"Found existing category: {category.name}")
            except Category.DoesNotExist:
                print(f"Could not find or create category: {cat_data['name']}")
                continue
    
    # Создание тегов
    tags_data = [
        {'name': 'Python', 'color': '#3776ab'},
        {'name': 'JavaScript', 'color': '#f7df1e'},
        {'name': 'Django', 'color': '#092e20'},
        {'name': 'Bestseller', 'color': '#ffd93d'},
        {'name': 'New', 'color': '#6bcf7f'},
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
                print(f"Created tag: {tag.name}")
            else:
                print(f"Tag already exists: {tag.name}")
        except Exception as e:
            print(f"Error creating tag {tag_data['name']}: {e}")
            try:
                tag = Tag.objects.get(name=tag_data['name'])
                tags.append(tag)
                print(f"Found existing tag: {tag.name}")
            except Tag.DoesNotExist:
                print(f"Could not find or create tag: {tag_data['name']}")
                continue
    
    # Создание тестовых книг
    books_data = [
        {
            'title': 'Python for Beginners',
            'author': 'Mark Lutz',
            'description': 'Comprehensive guide to learning Python from scratch. The book covers all the basic concepts of the Python programming language.',
            'category': 'Programming',
            'tags': ['Python', 'Bestseller']
        },
        {
            'title': 'JavaScript: The Definitive Guide',
            'author': 'David Flanagan',
            'description': 'Comprehensive guide to JavaScript for experienced programmers.',
            'category': 'Programming',
            'tags': ['JavaScript', 'Bestseller']
        },
        {
            'title': 'Django 4 by Example',
            'author': 'Antonio Mele',
            'description': 'Practical guide to creating web applications using Django 4.',
            'category': 'Programming',
            'tags': ['Django', 'Python', 'New']
        },
        {
            'title': 'Web Design for Beginners',
            'author': 'Jon Duckett',
            'description': 'Complete guide to HTML5 and CSS3 for creating modern websites.',
            'category': 'Design',
            'tags': ['New']
        },
        {
            'title': 'The Startup Owner\'s Manual',
            'author': 'Steve Blank',
            'description': 'Practical guide to creating a successful startup.',
            'category': 'Business',
            'tags': ['Bestseller']
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
                
                print(f"Created book: {book.title}")
            else:
                print(f"Book already exists: {book.title}")
        except Exception as e:
            print(f"Error creating book {book_data['title']}: {e}")
            continue
    
    print(f"\nStatistics:")
    print(f"   Categories: {Category.objects.count()}")
    print(f"   Tags: {Tag.objects.count()}")
    print(f"   Books: {Book.objects.count()}")

def main():
    """Основная функция"""
    print("=" * 60)
    print("FIXING BOOKS DATABASE")
    print("=" * 60)
    
    try:
        # Создание таблиц
        create_tables()
        
        # Создание тестовых данных
        create_sample_data()
        
        print("\n" + "=" * 60)
        print("FIXING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Now you can go to:")
        print("   http://127.0.0.1:8001/books/")
        print("\nAvailable features:")
        print("   • Browse book catalog")
        print("   • Read PDF online")
        print("   • Search and filter")
        print("   • Classification by categories and tags")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to exit...")

if __name__ == '__main__':
    main()