@echo off
chcp 65001
title Check Books Data

echo.
echo ========================================
echo    CHECKING BOOKS DATA
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
echo [2/2] Checking data...
python check_data.py

echo.
echo ========================================
echo    CHECK COMPLETED
echo ========================================
echo.
pause

