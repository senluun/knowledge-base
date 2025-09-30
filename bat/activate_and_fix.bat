@echo off
chcp 65001
title Activate Virtual Environment and Fix Database

echo.
echo ========================================
echo    ACTIVATING VIRTUAL ENVIRONMENT
echo ========================================
echo.

echo [1/3] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [2/3] Creating migrations...
python manage.py makemigrations books

echo.
echo [3/3] Applying migrations...
python manage.py migrate

echo.
echo [4/4] Creating sample data...
python fix_books_database.py

echo.
echo ========================================
echo    DONE! Now go to:
echo    http://127.0.0.1:8001/books/
echo ========================================
echo.
pause

