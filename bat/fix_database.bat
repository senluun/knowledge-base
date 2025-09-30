@echo off
chcp 65001
title Fix Books Database

echo.
echo ========================================
echo    FIXING BOOKS DATABASE
echo ========================================
echo.

echo [1/4] Activating virtual environment...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Virtual environment not found, using system Python
)

echo.
echo [2/4] Creating migrations...
python manage.py makemigrations books

echo.
echo [3/4] Applying migrations...
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
