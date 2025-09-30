@echo off
chcp 65001 >nul
echo ========================================
echo ОТЛАДКА ПОРТОВ И СЕРВЕРА
echo ========================================

echo 1. Проверка порта 3000 ДО запуска:
netstat -ano | find ":3000"
echo.

echo 2. Активация .venv:
call .venv\Scripts\activate.bat

echo 3. Запуск сервера в фоне:
start /B python manage.py runserver 127.0.0.1:3000

echo 4. Ожидание 2 секунды:
timeout /t 2 /nobreak >nul

echo 5. Проверка порта 3000 ПОСЛЕ запуска:
netstat -ano | find ":3000"
echo.

echo 6. Проверка процессов Python:
tasklist | findstr python
echo.

echo 7. Попытка подключения:
curl -I http://127.0.0.1:3000/ 2>nul
if errorlevel 1 (
    echo Сайт недоступен через curl
) else (
    echo Сайт доступен через curl!
)
echo.

echo 8. Попытка через PowerShell:
powershell -Command "try { (Invoke-WebRequest -Uri http://127.0.0.1:3000/ -UseBasicParsing -TimeoutSec 5).StatusCode } catch { $_.Exception.Message }"
echo.

echo 9. Убиваю процессы Python:
taskkill /f /im python.exe 2>nul

echo 10. Попытка запуска на порту 5000:
echo ========================================
echo ЗАПУСКАЮ НА ПОРТУ 5000
echo ОТКРОЙТЕ: http://127.0.0.1:5000/
echo ========================================
python manage.py runserver 127.0.0.1:5000

pause
