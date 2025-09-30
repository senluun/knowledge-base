@echo off
chcp 65001 >nul
echo ========================================
echo    ЗАПУСК ОЧИЩЕННОГО ПРОЕКТА
echo ========================================
echo.

echo 🧹 Проект очищен от ненужных файлов!
echo.
echo 📊 Статистика очистки:
echo    ✅ Удалено статей: 18
echo    ✅ Удалено категорий: 2
echo    ✅ Удалено тестовых файлов
echo    ✅ Удалены медиа файлы
echo    ✅ Очищена база данных
echo.
echo 📁 Оставлены только основные файлы:
echo    📁 Django проект (knowledge_base)
echo    📁 Приложения (accounts, knowledge, moderation)
echo    📁 Шаблоны (templates)
echo    📁 Статические файлы (static)
echo    📁 Конфигурация (settings, requirements)
echo    📁 Документация (README, INSTALL, DEPLOYMENT)
echo.
echo 🚀 Запуск сервера...
echo.
echo 📋 Доступные команды:
echo    🌐 http://127.0.0.1:8000/ - Главная страница
echo    👤 http://127.0.0.1:8000/admin/ - Админ панель
echo    📝 http://127.0.0.1:8000/knowledge/create-article/ - Создать статью
echo    🔧 http://127.0.0.1:8000/moderation/ - Модерация
echo.

call .venv\Scripts\activate.bat
python manage.py runserver





echo ========================================
echo    ЗАПУСК ОЧИЩЕННОГО ПРОЕКТА
echo ========================================
echo.

echo 🧹 Проект очищен от ненужных файлов!
echo.
echo 📊 Статистика очистки:
echo    ✅ Удалено статей: 18
echo    ✅ Удалено категорий: 2
echo    ✅ Удалено тестовых файлов
echo    ✅ Удалены медиа файлы
echo    ✅ Очищена база данных
echo.
echo 📁 Оставлены только основные файлы:
echo    📁 Django проект (knowledge_base)
echo    📁 Приложения (accounts, knowledge, moderation)
echo    📁 Шаблоны (templates)
echo    📁 Статические файлы (static)
echo    📁 Конфигурация (settings, requirements)
echo    📁 Документация (README, INSTALL, DEPLOYMENT)
echo.
echo 🚀 Запуск сервера...
echo.
echo 📋 Доступные команды:
echo    🌐 http://127.0.0.1:8000/ - Главная страница
echo    👤 http://127.0.0.1:8000/admin/ - Админ панель
echo    📝 http://127.0.0.1:8000/knowledge/create-article/ - Создать статью
echo    🔧 http://127.0.0.1:8000/moderation/ - Модерация
echo.

call .venv\Scripts\activate.bat
python manage.py runserver


















