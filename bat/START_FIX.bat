@echo off
chcp 65001
title Fix Books Database

echo.
echo ========================================
echo    FIXING BOOKS DATABASE
echo ========================================
echo.

echo [1/2] Activating virtual environment...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Virtual environment not found, using system Python
)

echo.
echo [2/2] Running fix script...
python start_fix.py

echo.
echo ========================================
echo    DONE! Now go to:
echo    http://127.0.0.1:8001/books/
echo ========================================
echo.
pause