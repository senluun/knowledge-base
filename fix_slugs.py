#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для исправления пустых slug в базе данных
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from books.models import Category, Tag, Book
from django.utils.text import slugify

def fix_slugs():
    """Исправление пустых slug"""
    print("Исправление пустых slug...")
    
    # Исправляем категории
    print("\nИсправление категорий:")
    for category in Category.objects.all():
        if not category.slug:
            old_slug = category.slug
            category.slug = slugify(category.name)
            category.save()
            print(f"  ✅ {category.name}: '{old_slug}' -> '{category.slug}'")
        else:
            print(f"  ℹ️ {category.name}: slug уже есть '{category.slug}'")
    
    # Исправляем книги
    print("\nИсправление книг:")
    for book in Book.objects.all():
        if not book.slug:
            old_slug = book.slug
            book.slug = slugify(book.title)
            book.save()
            print(f"  ✅ {book.title}: '{old_slug}' -> '{book.slug}'")
        else:
            print(f"  ℹ️ {book.title}: slug уже есть '{book.slug}'")
    
    # Удаляем дублирующиеся категории
    print("\nУдаление дублирующихся категорий:")
    categories_to_remove = []
    
    # Находим дублирующиеся категории
    category_names = {}
    for category in Category.objects.all():
        name_lower = category.name.lower()
        if name_lower in category_names:
            # Находим дубликат
            existing_category = category_names[name_lower]
            if existing_category.slug and not category.slug:
                # Удаляем категорию без slug
                categories_to_remove.append(category)
                print(f"  🗑️ Удаляем дубликат: {category.name} (без slug)")
            elif not existing_category.slug and category.slug:
                # Удаляем существующую категорию без slug
                categories_to_remove.append(existing_category)
                print(f"  🗑️ Удаляем дубликат: {existing_category.name} (без slug)")
        else:
            category_names[name_lower] = category
    
    # Удаляем найденные дубликаты
    for category in categories_to_remove:
        # Перемещаем книги в основную категорию
        main_category = None
        for cat in Category.objects.all():
            if cat.name.lower() == category.name.lower() and cat.slug:
                main_category = cat
                break
        
        if main_category:
            # Перемещаем книги
            books_to_move = Book.objects.filter(category=category)
            for book in books_to_move:
                book.category = main_category
                book.save()
                print(f"    📚 Перемещена книга '{book.title}' в категорию '{main_category.name}'")
        
        # Удаляем дубликат
        category.delete()
        print(f"  ✅ Удалена дублирующаяся категория: {category.name}")
    
    print(f"\nИтоговая статистика:")
    print(f"  Категорий: {Category.objects.count()}")
    print(f"  Тегов: {Tag.objects.count()}")
    print(f"  Книг: {Book.objects.count()}")
    
    print("\nПроверка slug:")
    for category in Category.objects.all():
        print(f"  - {category.name}: '{category.slug}'")

if __name__ == '__main__':
    fix_slugs()
    input("\nНажмите Enter для выхода...")

