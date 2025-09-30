@echo off
chcp 65001
title Final Update

echo.
echo ========================================
echo    FINAL UPDATE
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
echo [2/2] Final update...
python final_update.py

echo.
echo ========================================
echo    FINAL UPDATE COMPLETED
echo ========================================
echo.
pause

