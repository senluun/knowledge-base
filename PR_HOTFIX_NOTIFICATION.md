# 🚨 HOTFIX: Критическая ошибка Notification

## Описание проблемы

**Ошибка:** `Notification() got unexpected keyword arguments: 'related_object_id'`

Эта критическая ошибка возникала при попытке сохранения статьи и отправки её на модерацию. Пользователи не могли создавать и отправлять статьи на рассмотрение.

## Причина

В модели `Notification` (файл `moderation/models.py`) отсутствует поле `related_object_id`, но код в `knowledge/views.py` пытался использовать этот несуществующий параметр при создании уведомления для модераторов.

## Что исправлено

### Файл: `knowledge/views.py` (строки 362-365)

**Было (❌ НЕПРАВИЛЬНО):**
```python
Notification.objects.create(
    user=moderator,
    title='Новая статья на рассмотрении',
    message=f'Пользователь {article.author.get_full_name()} создал новую статью "{article.title}" и отправил её на рассмотрение.',
    notification_type='new_article',
    related_object_id=article.id  # ❌ Этого поля НЕТ в модели!
)
```

**Стало (✅ ПРАВИЛЬНО):**
```python
Notification.objects.create(
    user=moderator,
    title='Новая статья на рассмотрении',
    message=f'Пользователь {article.author.get_full_name()} создал новую статью "{article.title}" и отправил её на рассмотрение.',
    notification_type='moderation_required'  # ✅ Корректный тип уведомления
)
```

## Изменения

- ❌ Удален несуществующий параметр `related_object_id`
- ✅ Изменен `notification_type` с `'new_article'` на `'moderation_required'` (существующий в NOTIFICATION_TYPES)
- ✅ Теперь используются только существующие поля модели Notification

## Тестирование

### До исправления:
```bash
# Попытка создать статью и отправить на модерацию
❌ TypeError: Notification() got unexpected keyword arguments: 'related_object_id'
```

### После исправления:
```bash
# Создание статьи и отправка на модерацию
✅ Статья успешно создана
✅ Уведомление отправлено модераторам
✅ Редирект на список предложений
```

## Как проверить

1. Войдите на сайт как обычный пользователь
2. Создайте новую статью
3. Выберите "Отправить на модерацию"
4. Убедитесь, что статья сохранилась без ошибок
5. Проверьте, что модераторы получили уведомление

## Модель Notification для справки

Существующие поля в модели `Notification`:
```python
class Notification(models.Model):
    user = models.ForeignKey(User, ...)
    notification_type = models.CharField(...)  # ✅
    title = models.CharField(...)              # ✅
    message = models.TextField(...)            # ✅
    is_read = models.BooleanField(...)
    created_at = models.DateTimeField(...)
    suggestion = models.ForeignKey(ContentSuggestion, ...)  # Опционально
    # related_object_id - НЕ СУЩЕСТВУЕТ! ❌
```

Допустимые значения `notification_type`:
- `'suggestion_approved'`
- `'suggestion_rejected'`
- `'suggestion_needs_revision'`
- `'new_suggestion'`
- `'moderation_required'` ✅ (используем это)
- `'system'`

## Приоритет

🔴 **CRITICAL** - Блокирует основную функциональность (создание статей)

## Связанные Issues

Closes #3
Fixes #notification-error

## Checklist

- [x] Код исправлен
- [x] Django check пройден (0 ошибок)
- [x] Изменения протестированы локально
- [x] Коммит создан с подробным описанием
- [x] Ветка запушена в GitHub
- [ ] Pull Request создан
- [ ] Код-ревью пройдено
- [ ] Смерджено в main
- [ ] Production обновлен
- [ ] Python кеш очищен на production (`./clear_cache.sh`)

## Deployment Notes

⚠️ **ВАЖНО:** После мержа в `main` и деплоя на production необходимо:

1. Очистить Python кеш:
   ```bash
   ./clear_cache.sh
   ```

2. Перезапустить Django сервер:
   ```bash
   # Development
   python manage.py runserver
   
   # Production (gunicorn)
   pkill -HUP gunicorn
   
   # Production (systemd)
   sudo systemctl restart your-service-name
   ```

3. Проверить работоспособность:
   - Создать тестовую статью
   - Отправить на модерацию
   - Убедиться в отсутствии ошибок

---

## Почему PR #2 не помог?

PR #2 был смержен **ДО** того, как было сделано это исправление. В PR #2 входил коммит `d9f6513`, который НЕ содержал исправления для Notification. Исправление было сделано позже в коммите `aa1d11d`, который остался в ветке `fix/create-article-editor-issues` и не попал в `main`.

## Branch Strategy

- `main` - стабильная ветка (содержит баг)
- `hotfix/notification-related-object-id` - исправление бага (этот PR)
- После мержа бага не будет в `main`
