#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для проверки данных в базе
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from books.models import Category, Tag, Book

def check_data():
    """Проверка данных в базе"""
    print("Проверка данных в базе...")
    
    # Проверяем категории
    print("\nКатегории:")
    for category in Category.objects.all():
        print(f"  - {category.name} (slug: '{category.slug}')")
        if not category.slug:
            print(f"    ❌ ПРОБЛЕМА: Пустой slug для категории {category.name}")
    
    # Проверяем теги
    print("\nТеги:")
    for tag in Tag.objects.all():
        print(f"  - {tag.name} (цвет: {tag.color})")
    
    # Проверяем книги
    print("\nКниги:")
    for book in Book.objects.all():
        print(f"  - {book.title} (slug: '{book.slug}')")
        if not book.slug:
            print(f"    ❌ ПРОБЛЕМА: Пустой slug для книги {book.title}")
    
    print(f"\nСтатистика:")
    print(f"  Категорий: {Category.objects.count()}")
    print(f"  Тегов: {Tag.objects.count()}")
    print(f"  Книг: {Book.objects.count()}")

if __name__ == '__main__':
    check_data()

