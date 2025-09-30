from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from knowledge.models import Article, Category

User = get_user_model()


class ContentSuggestion(models.Model):
    """Модель для предложений контента"""
    
    SUGGESTION_TYPES = [
        ('article', 'Статья'),
        ('category', 'Категория'),
        ('tag', 'Тег'),
        ('edit', 'Редактирование'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
        ('needs_revision', 'Требует доработки'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('urgent', 'Срочный'),
    ]
    
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    suggestion_type = models.CharField('Тип предложения', max_length=20, choices=SUGGESTION_TYPES)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField('Приоритет', max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_suggestions')
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderated_suggestions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    target_article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)
    
    tags = models.CharField('Теги', max_length=500, blank=True)
    moderator_comment = models.TextField('Комментарий модератора', blank=True)
    
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    moderated_at = models.DateTimeField('Модерировано', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Предложение контента'
        verbose_name_plural = 'Предложения контента'
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class ModerationLog(models.Model):
    """Модель для логов модерации"""
    
    ACTION_CHOICES = [
        ('created', 'Создано'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
        ('needs_revision', 'Требует доработки'),
        ('edited', 'Отредактировано'),
        ('deleted', 'Удалено'),
    ]
    
    suggestion = models.ForeignKey(ContentSuggestion, on_delete=models.CASCADE, related_name='moderation_logs')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField('Действие', max_length=20, choices=ACTION_CHOICES)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Лог модерации'
        verbose_name_plural = 'Логи модерации'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.suggestion.title} - {self.get_action_display()}"


class Notification(models.Model):
    """Модель для уведомлений"""
    
    NOTIFICATION_TYPES = [
        ('suggestion_approved', 'Предложение одобрено'),
        ('suggestion_rejected', 'Предложение отклонено'),
        ('suggestion_needs_revision', 'Предложение требует доработки'),
        ('new_suggestion', 'Новое предложение'),
        ('moderation_required', 'Требуется модерация'),
        ('system', 'Системное уведомление'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField('Тип уведомления', max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField('Заголовок', max_length=200)
    message = models.TextField('Сообщение')
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    # Связь с предложением (если применимо)
    suggestion = models.ForeignKey(ContentSuggestion, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
