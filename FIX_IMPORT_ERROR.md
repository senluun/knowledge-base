# 🔧 Исправление ошибки ImportError в books.views

## Ошибка
```
ImportError: cannot import name 'Article' from 'books.models'
```

## Причина
У вас на локальной машине **устаревшая версия кода**. В старой версии `books/views.py` был неправильный импорт, который уже исправлен в репозитории.

## ✅ Решение (выберите один из вариантов)

### Вариант 1: Обновить код из GitHub (РЕКОМЕНДУЕТСЯ)

```bash
# 1. Сохраните все незакоммиченные изменения
git stash

# 2. Обновите код из GitHub
git checkout main
git pull origin main

# 3. Верните ваши изменения (если были)
git stash pop

# 4. Очистите Python кеш
# Windows PowerShell:
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force

# Windows CMD:
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
del /s /q *.pyc

# Linux/Mac:
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete

# 5. Перезапустите сервер
python manage.py runserver 8001
```

### Вариант 2: Ручное исправление файла

Если вы не можете обновиться из Git, исправьте файл вручную:

**Файл:** `books/views.py`

**Найдите строку (примерно строка 16):**
```python
from .models import Category, Article, Comment, ArticleView, Favorite, ArticleAttachment
```

**Замените на:**
```python
from .models import Book, Category, Tag, BookView
```

Затем очистите кеш и перезапустите сервер (см. шаг 4-5 выше).

---

## Проверка исправления

После выполнения шагов выше:

1. Запустите сервер:
   ```bash
   python manage.py runserver 8001
   ```

2. Убедитесь, что нет ошибок ImportError

3. Откройте в браузере: http://127.0.0.1:8001

---

## Если проблема сохраняется

### Проверьте правильность импортов:

```bash
# Проверьте, что в books/views.py правильные импорты
python -c "from books.models import Book, Category, Tag, BookView; print('✅ Импорты правильные')"
```

Должно вывести: `✅ Импорты правильные`

Если ошибка, значит проблема в файле `books/models.py` - проверьте, что там определены эти модели.

### Проверьте, какие модели есть в books.models:

```bash
python manage.py shell
```

В shell выполните:
```python
from books import models
print(dir(models))
# Должны быть: Book, Category, Tag, BookView
```

---

## Дополнительная диагностика

Если после всех шагов проблема остается:

1. **Проверьте версию кода:**
   ```bash
   git log --oneline -5
   ```
   Убедитесь, что у вас последние коммиты

2. **Проверьте ветку:**
   ```bash
   git branch
   ```
   Вы должны быть на ветке `main` или `hotfix/notification-related-object-id`

3. **Проверьте статус Git:**
   ```bash
   git status
   ```
   Не должно быть незакоммиченных изменений в `books/views.py`

4. **Пересоздайте виртуальное окружение:**
   ```bash
   # Удалите старое
   # Windows:
   rmdir /s venv
   
   # Linux/Mac:
   rm -rf venv
   
   # Создайте новое
   python -m venv venv
   
   # Активируйте
   # Windows:
   venv\Scripts\activate
   
   # Linux/Mac:
   source venv/bin/activate
   
   # Установите зависимости
   pip install -r requirements.txt
   ```

---

## Контрольный список

- [ ] Код обновлен из Git (`git pull origin main`)
- [ ] Python кеш очищен (удалены `__pycache__` и `*.pyc`)
- [ ] Виртуальное окружение активировано
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] Миграции применены (`python manage.py migrate`)
- [ ] Статические файлы собраны (`python manage.py collectstatic --noinput`)
- [ ] Сервер перезапущен
- [ ] Ошибка исчезла ✅

---

## Для продвинутых пользователей

Если вы уверены, что код актуальный, но ошибка остается:

```bash
# Жесткий сброс до состояния origin/main
git fetch origin
git reset --hard origin/main

# Очистка всех неотслеживаемых файлов (ОСТОРОЖНО!)
git clean -fdx

# Переустановка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate

# Запуск сервера
python manage.py runserver 8001
```

⚠️ **ВНИМАНИЕ:** `git reset --hard` и `git clean -fdx` удалят все ваши локальные изменения!
