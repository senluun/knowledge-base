@echo off
chcp 65001 >nul
echo ========================================
echo ПРОВЕРКА ПОДКЛЮЧЕНИЯ К САЙТУ
echo ========================================

echo 1. Проверка процессов Python:
tasklist | findstr python
echo.

echo 2. Проверка порта 8000:
netstat -ano | find ":8000"
echo.

echo 3. Проверка доступности через curl:
curl -I http://127.0.0.1:8000/ 2>nul
if errorlevel 1 (
    echo curl не работает, пробую PowerShell:
    powershell -Command "try { (Invoke-WebRequest -Uri http://127.0.0.1:8000/ -UseBasicParsing).StatusCode } catch { $_.Exception.Message }"
) else (
    echo Сайт доступен через curl!
)
echo.

echo 4. Запуск сервера в фоне:
echo ========================================
echo ЗАПУСКАЮ СЕРВЕР В ФОНЕ
echo Откройте браузер: http://127.0.0.1:8000/knowledge/
echo ========================================
start /B python manage.py runserver 127.0.0.1:8000

echo 5. Ожидание 3 секунды...
timeout /t 3 /nobreak >nul

echo 6. Проверка доступности после запуска:
curl -I http://127.0.0.1:8000/ 2>nul
if errorlevel 1 (
    echo Сайт все еще недоступен!
    echo Проверьте, что в окне cmd запущен сервер
) else (
    echo Сайт доступен!
)

echo.
echo 7. Проверка порта 8000 после запуска:
netstat -ano | find ":8000"
echo.

pause
