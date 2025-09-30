@echo off
echo ========================================
echo    Настройка библиотеки книг
echo ========================================
echo.

echo [1/4] Применение миграций...
python manage.py makemigrations books
python manage.py migrate

echo.
echo [2/4] Создание тестовых данных...
python create_sample_books.py

echo.
echo [3/4] Сбор статических файлов...
python manage.py collectstatic --noinput

echo.
echo [4/4] Создание папок для медиа файлов...
if not exist "media\books\covers" mkdir "media\books\covers"
if not exist "media\books\pdfs" mkdir "media\books\pdfs"

echo.
echo ========================================
echo    Настройка завершена!
echo ========================================
echo.
echo Доступные URL:
echo - Библиотека книг: http://localhost:8000/books/
echo - Админ панель: http://localhost:8000/admin/
echo.
echo Для запуска сервера выполните:
echo python manage.py runserver
echo.
pause

