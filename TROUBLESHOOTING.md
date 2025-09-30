# 🔧 Решение проблем / Troubleshooting

## Ошибка: `Notification() got unexpected keyword arguments: 'related_object_id'`

### Причина
Ошибка возникает из-за использования кешированного Python-кода (`.pyc` файлов), в котором еще содержится старый код с параметром `related_object_id`.

### ✅ Решение

#### Вариант 1: Автоматическая очистка (рекомендуется)
```bash
# Запустите скрипт очистки кеша
./clear_cache.sh

# Перезапустите Django сервер
python manage.py runserver
```

#### Вариант 2: Ручная очистка
```bash
# 1. Очистите все __pycache__ директории
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# 2. Удалите все .pyc файлы
find . -name "*.pyc" -delete

# 3. Удалите все .pyo файлы
find . -name "*.pyo" -delete

# 4. Перезапустите Django сервер
python manage.py runserver
```

#### Вариант 3: Перезапуск production-сервера
Если используете gunicorn/uwsgi/systemd:
```bash
# gunicorn
pkill -HUP gunicorn

# systemd
sudo systemctl restart your-service-name

# uwsgi
touch /path/to/uwsgi.ini  # touch для reload
```

### Что было исправлено
В файле `knowledge/views.py` (коммит `aa1d11d`):
```python
# Было (НЕПРАВИЛЬНО):
Notification.objects.create(
    user=moderator,
    title='Новая статья на рассмотрении',
    message=f'...',
    notification_type='new_article',
    related_object_id=article.id  # ❌ Этого поля нет в модели!
)

# Стало (ПРАВИЛЬНО):
Notification.objects.create(
    user=moderator,
    title='Новая статья на рассмотрении',
    message=f'...',
    notification_type='moderation_required'  # ✅ Только разрешенные поля
)
```

### Проверка исправления
После очистки кеша и перезапуска проверьте:
1. Создайте новую статью
2. Отправьте её на модерацию
3. Убедитесь, что ошибка не возникает

---

## Другие распространенные проблемы

### Статические файлы не обновляются
```bash
# Пересоберите статические файлы
python manage.py collectstatic --noinput --clear

# Очистите кеш браузера (Ctrl+Shift+R или Cmd+Shift+R)
```

### CSS/JS изменения не применяются
1. Проверьте, что файлы в `static/` изменены
2. Запустите `collectstatic`
3. Очистите кеш браузера (Hard Refresh)
4. Проверьте настройку `STATICFILES_DIRS` в settings.py

### Миграции не применяются
```bash
# Проверьте статус миграций
python manage.py showmigrations

# Примените миграции
python manage.py migrate
```

---

## 📞 Поддержка
Если проблема сохраняется:
1. Проверьте логи сервера
2. Убедитесь, что используете последнюю версию кода (git pull)
3. Проверьте права доступа к файлам
4. Создайте issue на GitHub с описанием проблемы
