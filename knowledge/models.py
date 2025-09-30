from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """Категории базы знаний"""
    
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Иконка')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='Цвет')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from .utils import slugify_cyrillic, create_unique_slug
            self.slug = create_unique_slug(Category, slugify_cyrillic(self.name))
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('knowledge:category_detail', kwargs={'slug': self.slug})


class Article(models.Model):
    """Статьи базы знаний"""
    
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('pending', 'На рассмотрении'),
        ('published', 'Опубликовано'),
        ('archived', 'Архив'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    excerpt = models.TextField(max_length=500, blank=True, verbose_name='Краткое описание')
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='articles',
        verbose_name='Категория'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='authored_articles',
        verbose_name='Автор'
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name='Статус'
    )
    tags = models.CharField(max_length=200, blank=True, verbose_name='Теги')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемая')
    allow_comments = models.BooleanField(default=True, verbose_name='Разрешить комментарии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата публикации')
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('knowledge:article_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    


class ArticleAttachment(models.Model):
    """Вложения к статьям"""
    
    FILE_TYPES = [
        ('image', 'Изображение'),
        ('document', 'Документ'),
        ('text', 'Текстовый файл'),
        ('csv', 'CSV файл'),
        ('other', 'Другое'),
    ]
    
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='attachments',
        verbose_name='Статья'
    )
    file = models.FileField(
        upload_to='attachments/%Y/%m/%d/',
        verbose_name='Файл'
    )
    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPES,
        verbose_name='Тип файла'
    )
    original_name = models.CharField(
        max_length=255,
        verbose_name='Оригинальное имя файла'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_attachments',
        verbose_name='Загрузил'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество скачиваний'
    )
    
    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.original_name} ({self.article.title})"
    
    def get_file_size(self):
        """Возвращает размер файла в читаемом формате"""
        try:
            size = self.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Неизвестно"
    
    def increment_downloads(self):
        """Увеличивает счетчик скачиваний"""
        self.download_count += 1
        self.save(update_fields=['download_count'])


class Comment(models.Model):
    """Комментарии к статьям"""
    
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Статья'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Автор'
    )
    content = models.TextField(verbose_name='Содержание')
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='replies',
        verbose_name='Родительский комментарий'
    )
    is_approved = models.BooleanField(default=True, verbose_name='Одобрен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Комментарий от {self.author.get_full_name()} к "{self.article.title}"'


class ArticleScreenshot(models.Model):
    """Скриншоты для статей"""
    
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='screenshots',
        verbose_name='Статья'
    )
    image = models.ImageField(
        upload_to='screenshots/%Y/%m/%d/', 
        verbose_name='Изображение'
    )
    title = models.CharField(max_length=200, blank=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f'Скриншот для "{self.article.title}"'


class ArticleView(models.Model):
    """Отслеживание просмотров статей"""
    
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='article_views',
        verbose_name='Статья'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='article_views',
        verbose_name='Пользователь'
    )
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')
    
    class Meta:
        verbose_name = 'Просмотр статьи'
        verbose_name_plural = 'Просмотры статей'
        ordering = ['-viewed_at']
        unique_together = ['article', 'user', 'ip_address']
    
    def __str__(self):
        return f'Просмотр "{self.article.title}" - {self.viewed_at}'


class Favorite(models.Model):
    """Избранные статьи пользователей"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='favorites',
        verbose_name='Пользователь'
    )
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='favorited_by',
        verbose_name='Статья'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ['user', 'article']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.get_full_name()} добавил в избранное "{self.article.title}"'
















