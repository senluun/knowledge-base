#!/usr/bin/env python
"""
Скрипт для создания тестовых данных библиотеки книг
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from books.models import Category, Tag, Book
from django.core.files.base import ContentFile
from django.utils.text import slugify

def create_sample_data():
    """Создание тестовых данных"""
    
    print("Создание категорий...")
    categories_data = [
        {
            'name': 'Программирование',
            'description': 'Книги по программированию и разработке ПО'
        },
        {
            'name': 'Дизайн',
            'description': 'Книги по веб-дизайну, UI/UX и графическому дизайну'
        },
        {
            'name': 'Бизнес',
            'description': 'Книги по бизнесу, менеджменту и предпринимательству'
        },
        {
            'name': 'Наука',
            'description': 'Научная литература и исследования'
        },
        {
            'name': 'Художественная литература',
            'description': 'Романы, рассказы и художественные произведения'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'slug': slugify(cat_data['name'])
            }
        )
        categories.append(category)
        if created:
            print(f"Создана категория: {category.name}")
    
    print("\nСоздание тегов...")
    tags_data = [
        {'name': 'Python', 'color': '#3776ab'},
        {'name': 'JavaScript', 'color': '#f7df1e'},
        {'name': 'Django', 'color': '#092e20'},
        {'name': 'React', 'color': '#61dafb'},
        {'name': 'HTML/CSS', 'color': '#e34f26'},
        {'name': 'Базы данных', 'color': '#336791'},
        {'name': 'Алгоритмы', 'color': '#ff6b6b'},
        {'name': 'Веб-разработка', 'color': '#4ecdc4'},
        {'name': 'Мобильная разработка', 'color': '#45b7d1'},
        {'name': 'DevOps', 'color': '#96ceb4'},
        {'name': 'Бестселлер', 'color': '#ffd93d'},
        {'name': 'Новинка', 'color': '#6bcf7f'},
        {'name': 'Классика', 'color': '#a8a8a8'},
        {'name': 'Для начинающих', 'color': '#ff9ff3'},
        {'name': 'Продвинутый уровень', 'color': '#54a0ff'}
    ]
    
    tags = []
    for tag_data in tags_data:
        tag, created = Tag.objects.get_or_create(
            name=tag_data['name'],
            defaults={'color': tag_data['color']}
        )
        tags.append(tag)
        if created:
            print(f"Создан тег: {tag.name}")
    
    print("\nСоздание тестовых книг...")
    
    # Создаем фиктивный PDF файл
    dummy_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
    
    books_data = [
        {
            'title': 'Python для начинающих',
            'author': 'Марк Лутц',
            'description': 'Подробное руководство по изучению Python с нуля. Книга охватывает все основные концепции языка программирования Python.',
            'category': 'Программирование',
            'tags': ['Python', 'Для начинающих', 'Бестселлер']
        },
        {
            'title': 'JavaScript: Подробное руководство',
            'author': 'Дэвид Флэнаган',
            'description': 'Исчерпывающее руководство по JavaScript. Книга для опытных программистов, которые хотят изучить JavaScript.',
            'category': 'Программирование',
            'tags': ['JavaScript', 'Продвинутый уровень', 'Бестселлер']
        },
        {
            'title': 'Django 4 в примерах',
            'author': 'Антонио Меле',
            'description': 'Практическое руководство по созданию веб-приложений с использованием Django 4.',
            'category': 'Программирование',
            'tags': ['Django', 'Python', 'Веб-разработка']
        },
        {
            'title': 'React в действии',
            'author': 'Марк Тилен Томас',
            'description': 'Современные методы разработки пользовательских интерфейсов с React.',
            'category': 'Программирование',
            'tags': ['React', 'JavaScript', 'Веб-разработка']
        },
        {
            'title': 'HTML и CSS. Дизайн и верстка веб-сайтов',
            'author': 'Джон Дакетт',
            'description': 'Полное руководство по HTML5 и CSS3 для создания современных веб-сайтов.',
            'category': 'Дизайн',
            'tags': ['HTML/CSS', 'Веб-разработка', 'Для начинающих']
        },
        {
            'title': 'Алгоритмы и структуры данных',
            'author': 'Томас Кормен',
            'description': 'Классический учебник по алгоритмам и структурам данных.',
            'category': 'Программирование',
            'tags': ['Алгоритмы', 'Продвинутый уровень', 'Классика']
        },
        {
            'title': 'Стартап. Настольная книга основателя',
            'author': 'Стив Бланк',
            'description': 'Практическое руководство по созданию успешного стартапа.',
            'category': 'Бизнес',
            'tags': ['Бестселлер', 'Новинка']
        },
        {
            'title': '1984',
            'author': 'Джордж Оруэлл',
            'description': 'Классический роман-антиутопия о тоталитарном обществе.',
            'category': 'Художественная литература',
            'tags': ['Классика', 'Бестселлер']
        }
    ]
    
    for book_data in books_data:
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
            
            print(f"Создана книга: {book.title}")
    
    print(f"\nСоздание завершено!")
    print(f"Категорий: {Category.objects.count()}")
    print(f"Тегов: {Tag.objects.count()}")
    print(f"Книг: {Book.objects.count()}")

if __name__ == '__main__':
    create_sample_data()

