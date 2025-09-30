@echo off
chcp 65001
title Исправление базы данных для библиотеки книг

echo.
echo ========================================
echo    ИСПРАВЛЕНИЕ БАЗЫ ДАННЫХ ДЛЯ КНИГ
echo ========================================
echo.

echo [1/2] Создание таблиц и данных...
python quick_fix.py

echo.
echo [2/2] Проверка результата...
python -c "import django; django.setup(); from books.models import Book; print(f'Книг в базе: {Book.objects.count()}')"

echo.
echo ========================================
echo    ГОТОВО! Теперь перейдите на:
echo    http://127.0.0.1:8001/books/
echo ========================================
echo.
pause

