#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для исправления slug с кириллическими символами
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

def fix_cyrillic_slugs():
    """Исправление slug с кириллическими символами"""
    print("Исправление slug с кириллическими символами...")
    
    # Исправляем категории
    print("\nИсправление категорий:")
    for category in Category.objects.all():
        if not category.slug:
            old_slug = category.slug
            category.slug = create_slug_for_cyrillic(category.name)
            category.save()
            print(f"  ✅ {category.name}: '{old_slug}' -> '{category.slug}'")
        else:
            print(f"  ℹ️ {category.name}: slug уже есть '{category.slug}'")
    
    # Исправляем книги
    print("\nИсправление книг:")
    for book in Book.objects.all():
        if not book.slug:
            old_slug = book.slug
            book.slug = create_slug_for_cyrillic(book.title)
            book.save()
            print(f"  ✅ {book.title}: '{old_slug}' -> '{book.slug}'")
        else:
            print(f"  ℹ️ {book.title}: slug уже есть '{book.slug}'")
    
    # Удаляем дублирующиеся категории
    print("\nУдаление дублирующихся категорий:")
    categories_to_remove = []
    
    # Находим дублирующиеся категории по смыслу
    programming_categories = []
    for category in Category.objects.all():
        if 'programming' in category.name.lower() or 'программирование' in category.name.lower():
            programming_categories.append(category)
    
    if len(programming_categories) > 1:
        # Оставляем категорию с slug, удаляем остальные
        main_category = None
        for cat in programming_categories:
            if cat.slug:
                main_category = cat
                break
        
        if main_category:
            for cat in programming_categories:
                if cat != main_category:
                    # Перемещаем книги
                    books_to_move = Book.objects.filter(category=cat)
                    for book in books_to_move:
                        book.category = main_category
                        book.save()
                        print(f"    📚 Перемещена книга '{book.title}' в категорию '{main_category.name}'")
                    
                    # Удаляем дубликат
                    cat.delete()
                    print(f"  ✅ Удалена дублирующаяся категория: {cat.name}")
    
    print(f"\nИтоговая статистика:")
    print(f"  Категорий: {Category.objects.count()}")
    print(f"  Тегов: {Tag.objects.count()}")
    print(f"  Книг: {Book.objects.count()}")
    
    print("\nПроверка slug:")
    for category in Category.objects.all():
        print(f"  - {category.name}: '{category.slug}'")

if __name__ == '__main__':
    fix_cyrillic_slugs()
    input("\nНажмите Enter для выхода...")

