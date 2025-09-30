@echo off
chcp 65001
echo ========================================
echo    ОБНОВЛЕНИЕ РЕПОЗИТОРИЯ НА GITHUB
echo ========================================
echo.

echo 📊 Проверяем статус изменений...
git status
echo.

echo 📁 Добавляем все изменения...
git add .
echo.

echo 📝 Создаем коммит...
git commit -m "Update project: added books library, automation scripts and improvements"
echo.

echo 🚀 Отправляем на GitHub...
git push
echo.

echo ✅ Проект успешно обновлен на GitHub!
echo 🌐 Репозиторий: https://github.com/senluun/knowledge-base
echo.
pause
