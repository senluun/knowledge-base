# База знаний

Веб-приложение для управления базой знаний с системой модерации контента.

## Возможности

### 🔐 Упрощенная система аутентификации:
- **Простая регистрация** - только Имя, Фамилия, Username
- **Email необязателен** - можно зарегистрироваться без email
- **Быстрый вход** по имени пользователя
- **Три роли:** Пользователь, Редактор, Администратор

### Для пользователей:
- Просмотр статей и категорий
- Поиск по базе знаний
- Добавление статей в избранное
- Комментирование статей
- Подача предложений на добавление контента

### Для редакторов:
- Создание и редактирование статей
- Модерация предложений пользователей
- Управление категориями

### Для администраторов:
- Полный доступ ко всем функциям
- Управление пользователями и ролями
- Аналитика и статистика

## 🚀 Установка и запуск

### Windows (Рекомендуемый способ):

**Автоматическая установка:**
```bash
# Просто запустите файл
install.bat
```

**Ручная установка:**
```bash
# Создание виртуального окружения
python -m venv .venv

# Активация виртуального окружения
.venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Инициализация с тестовыми данными
python manage.py init_project
```

**Запуск сервера:**
```bash
# Используйте готовый скрипт
start.bat

# Или вручную
.venv\Scripts\activate
python manage.py runserver
```

### Linux/Mac:

```bash
# Создание виртуального окружения
python3 -m venv .venv

# Активация виртуального окружения
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Инициализация с тестовыми данными
python manage.py init_project

# Запуск сервера
python manage.py runserver
```

### 🐳 Docker (Альтернативный способ):

```bash
# Запуск с Docker Compose
docker-compose up -d

# Выполнение миграций
docker-compose exec web python manage.py migrate --settings=knowledge_base.settings_prod
docker-compose exec web python manage.py init_project --settings=knowledge_base.settings_prod
```

### 🚫 Офлайн развертывание (без интернета):

**Для сервера без интернета:**

1. **На машине с интернетом** создайте офлайн пакет:
   ```bash
   chmod +x prepare-offline.sh
   ./prepare-offline.sh
   ```

2. **Скопируйте архив** на сервер без интернета

3. **На сервере** разверните:
   ```bash
   tar -xzf knowledge-base-offline-*.tar.gz
   cd knowledge-base-offline-*
   chmod +x offline-deploy.sh
   ./offline-deploy.sh
   ```

**Для Windows без интернета:**
```bash
# Используйте офлайн установку
install-offline.bat

# Запуск в офлайн режиме
start-offline.bat
```

**Сайт будет доступен по адресу:** http://localhost:8000

### 🔧 Решение проблем:

**Проблема:** "Couldn't import Django"
**Решение:** Убедитесь, что виртуальное окружение активировано:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac  
source .venv/bin/activate
```

**Проблема:** Ошибки кодировки в терминале Windows
**Решение:** Используйте готовые bat файлы (`install.bat`, `start.bat`)

**Проблема:** "The directory 'static' does not exist"
**Решение:** Автоматически создается при запуске `install.bat`

**Проблема:** "URL namespace 'knowledge' isn't unique"
**Решение:** Исправлено в обновленной версии urls.py

**Проблема:** "unique_together refers to nonexistent field"
**Решение:** Исправлено в модели ArticleView

**Проблема:** "Не удалось создать миграции"
**Решение:** 
1. Запустите `install.bat` - он исправит все проблемы автоматически
2. Если ошибки остаются, проверьте модели на синтаксические ошибки

**Проблема:** "такой таблицы нет: accounts_user" или "такой таблицы нет: knowledge_category"
**Решение:** 
1. **ЭКСТРЕННО:** Запустите `reset-database.bat` для полного сброса и пересоздания базы данных
2. Проверьте результат: `verify-database.bat`
3. После исправления запустите: `quick-start.bat`

**Проблема:** "InconsistentMigrationHistory" - конфликт миграций
**Решение:** 
1. **СРОЧНО:** Запустите `reset-database.bat` для полного сброса базы данных
2. Это удалит все старые миграции и создаст новые

**Проблема:** "TemplateDoesNotExist" - отсутствует шаблон
**Решение:** 
1. Все необходимые шаблоны уже созданы
2. Проверьте работу: `test-templates.bat`
3. Если ошибка остается, перезапустите сервер

**Проблема:** Ошибки с системой аутентификации
**Решение:** 
1. Обновите систему: `update-auth-system.bat`
2. Протестируйте: `test-auth.bat`
3. Перезапустите сервер: `quick-start.bat`

**Проблема:** "TemplateDoesNotExist" для accounts шаблонов
**Решение:** 
1. Все шаблоны accounts созданы
2. Проверьте работу: `test-accounts-templates.bat`
3. Перезапустите сервер: `quick-start.bat`

## Структура проекта

```
knowledge_base/
├── accounts/          # Управление пользователями
├── knowledge/         # База знаний
├── moderation/        # Система модерации
├── templates/         # HTML шаблоны
├── static/           # Статические файлы
└── media/            # Загруженные файлы
```

## Роли пользователей

- **Пользователь** - просмотр контента, комментирование, подача предложений
- **Редактор** - создание статей, модерация предложений
- **Администратор** - полный доступ ко всем функциям

## API

Проект использует Django REST Framework для API endpoints.

## Технологии

- Django 4.2
- Django REST Framework
- Bootstrap 5
- Font Awesome
- SQLite/PostgreSQL
















