#!/bin/bash
# Скрипт для очистки кеша Python и перезапуска Django сервера

echo "🔄 Очистка Python кеша..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

echo "✅ Кеш очищен!"
echo ""
echo "📝 Теперь перезапустите Django сервер:"
echo "   1. Остановите текущий процесс (Ctrl+C)"
echo "   2. Запустите заново: python manage.py runserver"
echo ""
echo "Или если используете gunicorn/uwsgi:"
echo "   sudo systemctl restart your-service-name"
