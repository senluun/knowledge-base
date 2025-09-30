#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Финальное обновление библиотеки книг
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from books.models import Category, Tag, Book
from django.utils.text import slugify

def create_slug_for_cyrillic(text):
    """Создание slug для кириллических текстов"""
    # Словарь для транслитерации
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    
    # Транслитерация
    result = ''
    for char in text:
        if char in translit_dict:
            result += translit_dict[char]
        else:
            result += char
    
    # Применяем стандартную slugify
    return slugify(result)

def update_final():
    """Финальное обновление библиотеки"""
    print("Финальное обновление библиотеки книг...")
    
    # Очищаем старые данные
    print("\nОчистка старых данных...")
    Book.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    
    # Создаем новые категории
    print("\nСоздание категорий...")
    categories_data = [
        {'name': 'Программирование', 'description': 'Книги по программированию и разработке ПО'},
        {'name': 'Дизайн', 'description': 'Книги по веб-дизайну и UI/UX'},
        {'name': 'Бизнес', 'description': 'Книги по бизнесу и менеджменту'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category.objects.create(
            name=cat_data['name'],
            description=cat_data['description'],
            slug=create_slug_for_cyrillic(cat_data['name'])
        )
        categories.append(category)
        print(f"  ✅ Создана категория: {category.name}")
    
    # Создаем теги
    print("\nСоздание тегов...")
    tags_data = [
        {'name': 'Python', 'color': '#3776ab'},
        {'name': 'JavaScript', 'color': '#f7df1e'},
        {'name': 'Django', 'color': '#092e20'},
        {'name': 'Бестселлер', 'color': '#ffd93d'},
        {'name': 'Новинка', 'color': '#6bcf7f'},
    ]
    
    tags = []
    for tag_data in tags_data:
        tag = Tag.objects.create(
            name=tag_data['name'],
            color=tag_data['color']
        )
        tags.append(tag)
        print(f"  ✅ Создан тег: {tag.name}")
    
    # Создаем книги
    print("\nСоздание книг...")
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
        # Находим категорию
        category = next(cat for cat in categories if cat.name == book_data['category'])
        
        # Создаем книгу
        book = Book.objects.create(
            title=book_data['title'],
            author=book_data['author'],
            description=book_data['description'],
            category=category,
            slug=create_slug_for_cyrillic(book_data['title']),
            is_published=True
        )
        
        # Создаем фиктивный PDF файл
        from django.core.files.base import ContentFile
        pdf_file = ContentFile(dummy_pdf_content, name=f"{create_slug_for_cyrillic(book_data['title'])}.pdf")
        book.pdf_file = pdf_file
        book.save()
        
        # Добавляем теги
        for tag_name in book_data['tags']:
            tag = next(tag for tag in tags if tag.name == tag_name)
            book.tags.add(tag)
        
        print(f"  ✅ Создана книга: {book.title}")
    
    print(f"\nИтоговая статистика:")
    print(f"  Категорий: {Category.objects.count()}")
    print(f"  Тегов: {Tag.objects.count()}")
    print(f"  Книг: {Book.objects.count()}")
    
    print("\nПроверка данных:")
    for category in Category.objects.all():
        print(f"  - Категория: {category.name} (slug: {category.slug})")
    
    for tag in Tag.objects.all():
        print(f"  - Тег: {tag.name}")
    
    for book in Book.objects.all():
        print(f"  - Книга: {book.title} (slug: {book.slug})")

if __name__ == '__main__':
    update_final()
    input("\nНажмите Enter для выхода...")

