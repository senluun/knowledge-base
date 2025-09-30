from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import ContentSuggestion, ModerationLog, Notification


@admin.register(ContentSuggestion)
class ContentSuggestionAdmin(admin.ModelAdmin):
    """Административная панель для предложений контента"""
    
    list_display = [
        'title', 'author', 'suggestion_type', 'status', 'priority', 
        'moderator', 'created_at', 'moderated_at'
    ]
    list_filter = [
        'status', 'suggestion_type', 'priority', 'created_at', 
        'moderated_at', 'category'
    ]
    search_fields = ['title', 'content', 'author__email', 'tags']
    raw_id_fields = ['author', 'moderator', 'category', 'target_article']
    date_hierarchy = 'created_at'
    ordering = ['-priority', '-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'suggestion_type', 'category', 'target_article')
        }),
        ('Автор и статус', {
            'fields': ('author', 'status', 'moderator', 'moderator_comment')
        }),
        ('Дополнительно', {
            'fields': ('tags', 'priority'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at', 'moderated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'author', 'moderator', 'category', 'target_article'
        )
    
    actions = [
        'approve_suggestions', 'reject_suggestions', 'request_revision',
        'change_status_to_pending', 'change_status_to_approved', 
        'change_status_to_rejected', 'change_status_to_needs_revision'
    ]
    
    def approve_suggestions(self, request, queryset):
        """Одобрить выбранные предложения"""
        updated = queryset.filter(status='pending').update(
            status='approved',
            moderator=request.user,
            moderated_at=timezone.now()
        )
        self.message_user(request, f'{updated} предложений одобрено.')
    approve_suggestions.short_description = 'Одобрить выбранные предложения'
    
    def reject_suggestions(self, request, queryset):
        """Отклонить выбранные предложения"""
        updated = queryset.filter(status='pending').update(
            status='rejected',
            moderator=request.user,
            moderated_at=timezone.now()
        )
        self.message_user(request, f'{updated} предложений отклонено.')
    reject_suggestions.short_description = 'Отклонить выбранные предложения'
    
    def request_revision(self, request, queryset):
        """Запросить доработку выбранных предложений"""
        updated = queryset.filter(status='pending').update(
            status='needs_revision',
            moderator=request.user,
            moderated_at=timezone.now()
        )
        self.message_user(request, f'{updated} предложений отправлено на доработку.')
    request_revision.short_description = 'Запросить доработку'
    
    def change_status_to_pending(self, request, queryset):
        """Перевести в статус 'На рассмотрении'"""
        updated = queryset.update(status='pending', moderator=None, moderated_at=None)
        self.message_user(request, f'{updated} предложений переведено в статус "На рассмотрении".')
    change_status_to_pending.short_description = 'Перевести в "На рассмотрении"'
    
    def change_status_to_approved(self, request, queryset):
        """Перевести в статус 'Одобрено'"""
        updated = queryset.update(
            status='approved',
            moderator=request.user,
            moderated_at=timezone.now()
        )
        self.message_user(request, f'{updated} предложений переведено в статус "Одобрено".')
    change_status_to_approved.short_description = 'Перевести в "Одобрено"'
    
    def change_status_to_rejected(self, request, queryset):
        """Перевести в статус 'Отклонено'"""
        updated = queryset.update(
            status='rejected',
            moderator=request.user,
            moderated_at=timezone.now()
        )
        self.message_user(request, f'{updated} предложений переведено в статус "Отклонено".')
    change_status_to_rejected.short_description = 'Перевести в "Отклонено"'
    
    def change_status_to_needs_revision(self, request, queryset):
        """Перевести в статус 'Требует доработки'"""
        updated = queryset.update(
            status='needs_revision',
            moderator=request.user,
            moderated_at=timezone.now()
        )
        self.message_user(request, f'{updated} предложений переведено в статус "Требует доработки".')
    change_status_to_needs_revision.short_description = 'Перевести в "Требует доработки"'


@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    """Административная панель для логов модерации"""
    
    list_display = ['suggestion', 'moderator', 'action', 'created_at']
    list_filter = ['action', 'created_at', 'moderator']
    search_fields = ['suggestion__title', 'moderator__email', 'comment']
    raw_id_fields = ['suggestion', 'moderator']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('suggestion', 'moderator')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Административная панель для уведомлений"""
    
    list_display = [
        'user', 'notification_type', 'title', 'is_read', 'created_at'
    ]
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__email', 'title', 'message']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    readonly_fields = ['created_at']
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Отметить как прочитанные"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} уведомлений отмечено как прочитанные.')
    mark_as_read.short_description = 'Отметить как прочитанные'
    
    def mark_as_unread(self, request, queryset):
        """Отметить как непрочитанные"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} уведомлений отмечено как непрочитанные.')
    mark_as_unread.short_description = 'Отметить как непрочитанные'
















