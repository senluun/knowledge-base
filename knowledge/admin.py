from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article, Comment, ArticleView, Favorite, ArticleAttachment
from .widgets import ProseMirrorAdminWidget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная панель для категорий"""
    
    list_display = ['name', 'slug', 'is_active', 'order', 'articles_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    def articles_count(self, obj):
        return obj.articles.count()
    articles_count.short_description = 'Количество статей'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Административная панель для статей"""
    
    list_display = [
        'title', 'category', 'author', 'status', 'views_count', 
        'is_featured', 'created_at', 'published_at'
    ]
    list_filter = ['status', 'category', 'is_featured', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'author', 'status')
        }),
        ('Содержание', {
            'fields': ('excerpt', 'content', 'tags')
        }),
        ('Настройки', {
            'fields': ('is_featured', 'views_count'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'views_count']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'author')
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = ProseMirrorAdminWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    actions = ['publish_articles', 'unpublish_articles', 'archive_articles', 'draft_articles']
    
    def publish_articles(self, request, queryset):
        """Опубликовать выбранные статьи"""
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} статей опубликовано.')
    publish_articles.short_description = 'Опубликовать выбранные статьи'
    
    def unpublish_articles(self, request, queryset):
        """Снять с публикации выбранные статьи"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} статей снято с публикации.')
    unpublish_articles.short_description = 'Снять с публикации'
    
    def archive_articles(self, request, queryset):
        """Архивировать выбранные статьи"""
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} статей архивировано.')
    archive_articles.short_description = 'Архивировать выбранные статьи'
    
    def draft_articles(self, request, queryset):
        """Перевести в черновики выбранные статьи"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} статей переведено в черновики.')
    draft_articles.short_description = 'Перевести в черновики'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Административная панель для комментариев"""
    
    list_display = [
        'article', 'author', 'content_preview', 'is_approved', 
        'parent', 'created_at'
    ]
    list_filter = ['is_approved', 'created_at', 'article__category']
    search_fields = ['content', 'author__email', 'article__title']
    raw_id_fields = ['article', 'author', 'parent']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Содержание'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('article', 'author')


@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    """Административная панель для просмотров статей"""
    
    list_display = ['article', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at', 'article__category']
    search_fields = ['article__title', 'user__email', 'ip_address']
    raw_id_fields = ['article', 'user']
    date_hierarchy = 'viewed_at'
    ordering = ['-viewed_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('article', 'user')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Административная панель для избранного"""
    
    list_display = ['user', 'article', 'created_at']
    list_filter = ['created_at', 'article__category']
    search_fields = ['user__email', 'article__title']
    raw_id_fields = ['user', 'article']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'article')


@admin.register(ArticleAttachment)
class ArticleAttachmentAdmin(admin.ModelAdmin):
    """Административная панель для вложений статей"""
    
    list_display = ['original_name', 'article', 'file_type', 'uploaded_by', 'download_count', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at', 'article__category']
    search_fields = ['original_name', 'article__title', 'uploaded_by__email']
    raw_id_fields = ['article', 'uploaded_by']
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('article', 'file', 'original_name', 'file_type')
        }),
        ('Дополнительно', {
            'fields': ('description', 'uploaded_by', 'download_count')
        }),
        ('Даты', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['uploaded_at', 'download_count']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('article', 'uploaded_by')
















