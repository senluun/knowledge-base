#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from knowledge.models import Article, Category, Comment, ArticleView, ArticleScreenshot, ArticleAttachment
from moderation.models import ContentSuggestion, ModerationLog, Notification
from accounts.models import User

def clear_database():
    print("🧹 Очистка базы данных...")
    
    # Удаляем все статьи и связанные данные
    print("📄 Удаление статей...")
    articles_count = Article.objects.count()
    Article.objects.all().delete()
    print(f"   ✅ Удалено статей: {articles_count}")
    
    # Удаляем все категории
    print("📁 Удаление категорий...")
    categories_count = Category.objects.count()
    Category.objects.all().delete()
    print(f"   ✅ Удалено категорий: {categories_count}")
    
    # Удаляем все комментарии
    print("💬 Удаление комментариев...")
    comments_count = Comment.objects.count()
    Comment.objects.all().delete()
    print(f"   ✅ Удалено комментариев: {comments_count}")
    
    # Удаляем все просмотры статей
    print("👁️ Удаление просмотров...")
    views_count = ArticleView.objects.count()
    ArticleView.objects.all().delete()
    print(f"   ✅ Удалено просмотров: {views_count}")
    
    # Удаляем все скриншоты
    print("🖼️ Удаление скриншотов...")
    screenshots_count = ArticleScreenshot.objects.count()
    ArticleScreenshot.objects.all().delete()
    print(f"   ✅ Удалено скриншотов: {screenshots_count}")
    
    # Удаляем все вложения
    print("📎 Удаление вложений...")
    attachments_count = ArticleAttachment.objects.count()
    ArticleAttachment.objects.all().delete()
    print(f"   ✅ Удалено вложений: {attachments_count}")
    
    # Удаляем все предложения контента
    print("📝 Удаление предложений...")
    suggestions_count = ContentSuggestion.objects.count()
    ContentSuggestion.objects.all().delete()
    print(f"   ✅ Удалено предложений: {suggestions_count}")
    
    # Удаляем все логи модерации
    print("📊 Удаление логов модерации...")
    logs_count = ModerationLog.objects.count()
    ModerationLog.objects.all().delete()
    print(f"   ✅ Удалено логов: {logs_count}")
    
    # Удаляем все уведомления
    print("🔔 Удаление уведомлений...")
    notifications_count = Notification.objects.count()
    Notification.objects.all().delete()
    print(f"   ✅ Удалено уведомлений: {notifications_count}")
    
    # Оставляем только админа
    print("👤 Очистка пользователей...")
    admin_users = User.objects.filter(is_superuser=True)
    other_users = User.objects.exclude(is_superuser=True)
    other_users_count = other_users.count()
    other_users.delete()
    print(f"   ✅ Удалено обычных пользователей: {other_users_count}")
    print(f"   ✅ Оставлено админов: {admin_users.count()}")
    
    print("\n🎉 База данных очищена!")
    print("📊 Статистика:")
    print(f"   📄 Статей: {Article.objects.count()}")
    print(f"   📁 Категорий: {Category.objects.count()}")
    print(f"   💬 Комментариев: {Comment.objects.count()}")
    print(f"   👁️ Просмотров: {ArticleView.objects.count()}")
    print(f"   🖼️ Скриншотов: {ArticleScreenshot.objects.count()}")
    print(f"   📎 Вложений: {ArticleAttachment.objects.count()}")
    print(f"   📝 Предложений: {ContentSuggestion.objects.count()}")
    print(f"   📊 Логов: {ModerationLog.objects.count()}")
    print(f"   🔔 Уведомлений: {Notification.objects.count()}")
    print(f"   👤 Пользователей: {User.objects.count()}")

if __name__ == "__main__":
    clear_database()




import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledge_base.settings')
django.setup()

from knowledge.models import Article, Category, Comment, ArticleView, ArticleScreenshot, ArticleAttachment
from moderation.models import ContentSuggestion, ModerationLog, Notification
from accounts.models import User

def clear_database():
    print("🧹 Очистка базы данных...")
    
    # Удаляем все статьи и связанные данные
    print("📄 Удаление статей...")
    articles_count = Article.objects.count()
    Article.objects.all().delete()
    print(f"   ✅ Удалено статей: {articles_count}")
    
    # Удаляем все категории
    print("📁 Удаление категорий...")
    categories_count = Category.objects.count()
    Category.objects.all().delete()
    print(f"   ✅ Удалено категорий: {categories_count}")
    
    # Удаляем все комментарии
    print("💬 Удаление комментариев...")
    comments_count = Comment.objects.count()
    Comment.objects.all().delete()
    print(f"   ✅ Удалено комментариев: {comments_count}")
    
    # Удаляем все просмотры статей
    print("👁️ Удаление просмотров...")
    views_count = ArticleView.objects.count()
    ArticleView.objects.all().delete()
    print(f"   ✅ Удалено просмотров: {views_count}")
    
    # Удаляем все скриншоты
    print("🖼️ Удаление скриншотов...")
    screenshots_count = ArticleScreenshot.objects.count()
    ArticleScreenshot.objects.all().delete()
    print(f"   ✅ Удалено скриншотов: {screenshots_count}")
    
    # Удаляем все вложения
    print("📎 Удаление вложений...")
    attachments_count = ArticleAttachment.objects.count()
    ArticleAttachment.objects.all().delete()
    print(f"   ✅ Удалено вложений: {attachments_count}")
    
    # Удаляем все предложения контента
    print("📝 Удаление предложений...")
    suggestions_count = ContentSuggestion.objects.count()
    ContentSuggestion.objects.all().delete()
    print(f"   ✅ Удалено предложений: {suggestions_count}")
    
    # Удаляем все логи модерации
    print("📊 Удаление логов модерации...")
    logs_count = ModerationLog.objects.count()
    ModerationLog.objects.all().delete()
    print(f"   ✅ Удалено логов: {logs_count}")
    
    # Удаляем все уведомления
    print("🔔 Удаление уведомлений...")
    notifications_count = Notification.objects.count()
    Notification.objects.all().delete()
    print(f"   ✅ Удалено уведомлений: {notifications_count}")
    
    # Оставляем только админа
    print("👤 Очистка пользователей...")
    admin_users = User.objects.filter(is_superuser=True)
    other_users = User.objects.exclude(is_superuser=True)
    other_users_count = other_users.count()
    other_users.delete()
    print(f"   ✅ Удалено обычных пользователей: {other_users_count}")
    print(f"   ✅ Оставлено админов: {admin_users.count()}")
    
    print("\n🎉 База данных очищена!")
    print("📊 Статистика:")
    print(f"   📄 Статей: {Article.objects.count()}")
    print(f"   📁 Категорий: {Category.objects.count()}")
    print(f"   💬 Комментариев: {Comment.objects.count()}")
    print(f"   👁️ Просмотров: {ArticleView.objects.count()}")
    print(f"   🖼️ Скриншотов: {ArticleScreenshot.objects.count()}")
    print(f"   📎 Вложений: {ArticleAttachment.objects.count()}")
    print(f"   📝 Предложений: {ContentSuggestion.objects.count()}")
    print(f"   📊 Логов: {ModerationLog.objects.count()}")
    print(f"   🔔 Уведомлений: {Notification.objects.count()}")
    print(f"   👤 Пользователей: {User.objects.count()}")

if __name__ == "__main__":
    clear_database()

















