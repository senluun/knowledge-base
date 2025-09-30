@echo off
chcp 65001
title Fix Empty Slugs

echo.
echo ========================================
echo    FIXING EMPTY SLUGS
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
echo [2/2] Fixing slugs...
python fix_slugs.py

echo.
echo ========================================
echo    SLUGS FIXED
echo ========================================
echo.
pause

