# Инструкция по добавлению проекта в GitHub

## Шаг 1: Подготовка локального репозитория

Выполните следующие команды в командной строке (cmd) или PowerShell:

```bash
# Добавить все файлы в Git
git add .

# Создать первый коммит
git commit -m "Initial commit: Django knowledge base project"

# Проверить статус
git status
```

## Шаг 2: Создание репозитория на GitHub

1. Перейдите на [GitHub.com](https://github.com)
2. Войдите в свой аккаунт
3. Нажмите кнопку "New" или "+" в правом верхнем углу
4. Выберите "New repository"
5. Заполните форму:
   - **Repository name**: `knowledge-base` (или любое другое имя)
   - **Description**: `Django Knowledge Base Project`
   - **Visibility**: Public или Private (на ваш выбор)
   - **НЕ** ставьте галочки на "Add a README file", "Add .gitignore", "Choose a license"
6. Нажмите "Create repository"

## Шаг 3: Подключение локального репозитория к GitHub

После создания репозитория на GitHub, выполните команды:

```bash
# Добавить удаленный репозиторий (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/knowledge-base.git

# Переименовать основную ветку в main
git branch -M main

# Отправить код на GitHub
git push -u origin main
```

## Шаг 4: Проверка

После выполнения всех команд:
1. Обновите страницу вашего репозитория на GitHub
2. Убедитесь, что все файлы загружены
3. Проверьте, что README.md отображается корректно

## Дополнительные команды

Если нужно добавить изменения в будущем:

```bash
# Добавить изменения
git add .

# Создать коммит
git commit -m "Описание изменений"

# Отправить на GitHub
git push
```

## Возможные проблемы

1. **Ошибка аутентификации**: Убедитесь, что вы авторизованы в Git
2. **Ошибка доступа**: Проверьте URL репозитория
3. **Конфликты**: Если репозиторий уже существует, используйте `git pull` перед `git push`

## Полезные ссылки

- [GitHub Docs](https://docs.github.com/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)
- [Django Documentation](https://docs.djangoproject.com/)
