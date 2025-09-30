@echo off
chcp 65001
title Update to Russian

echo.
echo ========================================
echo    UPDATE TO RUSSIAN
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
echo [2/2] Updating to Russian...
python update_to_russian.py

echo.
echo ========================================
echo    UPDATE COMPLETED
echo ========================================
echo.
pause

