#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для обновления данных на русский язык
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

def update_to_russian():
    """Обновление данных на русский язык"""
    print("Обновление данных на русский язык...")
    
    # Обновляем категории
    print("\nОбновление категорий:")
    category_updates = {
        'Programming': 'Программирование',
        'Design': 'Дизайн',
        'Business': 'Бизнес'
    }
    
    for old_name, new_name in category_updates.items():
        try:
            category = Category.objects.get(name=old_name)
            category.name = new_name
            category.slug = create_slug_for_cyrillic(new_name)
            category.save()
            print(f"  ✅ {old_name} -> {new_name}")
        except Category.DoesNotExist:
            print(f"  ℹ️ Категория {old_name} не найдена")
    
    # Обновляем теги
    print("\nОбновление тегов:")
    tag_updates = {
        'Python': 'Python',
        'JavaScript': 'JavaScript', 
        'Django': 'Django',
        'Bestseller': 'Бестселлер',
        'New': 'Новинка'
    }
    
    for old_name, new_name in tag_updates.items():
        try:
            tag = Tag.objects.get(name=old_name)
            tag.name = new_name
            tag.save()
            print(f"  ✅ {old_name} -> {new_name}")
        except Tag.DoesNotExist:
            print(f"  ℹ️ Тег {old_name} не найден")
    
    # Обновляем книги
    print("\nОбновление книг:")
    book_updates = {
        'Python for Beginners': 'Python для начинающих',
        'JavaScript: The Definitive Guide': 'JavaScript: Подробное руководство',
        'Django 4 by Example': 'Django 4 в примерах',
        'Web Design for Beginners': 'Веб-дизайн для начинающих',
        'The Startup Owner\'s Manual': 'Стартап. Настольная книга основателя'
    }
    
    for old_title, new_title in book_updates.items():
        try:
            book = Book.objects.get(title=old_title)
            book.title = new_title
            book.slug = create_slug_for_cyrillic(new_title)
            book.save()
            print(f"  ✅ {old_title} -> {new_title}")
        except Book.DoesNotExist:
            print(f"  ℹ️ Книга {old_title} не найдена")
    
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
    update_to_russian()
    input("\nНажмите Enter для выхода...")

