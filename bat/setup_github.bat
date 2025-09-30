@echo off
chcp 65001
echo Настройка Git репозитория для GitHub...
echo.

echo Добавляем файлы в Git...
git add .
if %errorlevel% neq 0 (
    echo Ошибка при добавлении файлов
    pause
    exit /b 1
)

echo.
echo Создаем первый коммит...
git commit -m "Initial commit: Django knowledge base project"
if %errorlevel% neq 0 (
    echo Ошибка при создании коммита
    pause
    exit /b 1
)

echo.
echo Git репозиторий готов!
echo.
echo Следующие шаги:
echo 1. Создайте репозиторий на GitHub.com
echo 2. Скопируйте URL репозитория
echo 3. Выполните команды:
echo    git remote add origin ^<URL_ВАШЕГО_РЕПОЗИТОРИЯ^>
echo    git branch -M main
echo    git push -u origin main
echo.
pause
