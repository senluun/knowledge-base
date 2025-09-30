@echo off
echo Testing Python...
python --version
if errorlevel 1 (
    echo Python not found!
) else (
    echo Python found!
)
pause
