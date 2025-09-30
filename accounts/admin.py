from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Административная панель для пользователей"""
    
    list_display = [
        'username', 'get_full_name', 'role', 'is_verified', 
        'is_active', 'date_joined', 'avatar_preview'
    ]
    list_filter = ['role', 'is_verified', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar', 'bio')
        }),
        ('Роли и права', {
            'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Группы и права', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 
                      'role', 'password1', 'password2'),
        }),
    )
    
    actions = ['make_editor', 'make_regular_user', 'make_admin', 'verify_users', 'unverify_users']
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="30" height="30" style="border-radius: 50%;" />',
                obj.avatar.url
            )
        return "Нет фото"
    avatar_preview.short_description = 'Аватар'
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Полное имя'
    
    def make_editor(self, request, queryset):
        """Назначить роль редактора"""
        updated = queryset.update(role='editor')
        self.message_user(request, f'{updated} пользователей назначены редакторами.')
    make_editor.short_description = "Назначить редакторами"
    
    def make_regular_user(self, request, queryset):
        """Назначить роль обычного пользователя"""
        updated = queryset.update(role='user')
        self.message_user(request, f'{updated} пользователей назначены обычными пользователями.')
    make_regular_user.short_description = "Назначить обычными пользователями"
    
    def make_admin(self, request, queryset):
        """Назначить роль администратора"""
        updated = queryset.update(role='admin', is_staff=True)
        self.message_user(request, f'{updated} пользователей назначены администраторами.')
    make_admin.short_description = "Назначить администраторами"
    
    def verify_users(self, request, queryset):
        """Верифицировать пользователей"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} пользователей верифицированы.')
    verify_users.short_description = "Верифицировать пользователей"
    
    def unverify_users(self, request, queryset):
        """Снять верификацию с пользователей"""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} пользователей сняты с верификации.')
    unverify_users.short_description = "Снять верификацию"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Административная панель для профилей пользователей"""
    
    list_display = ['user', 'department', 'position', 'experience_years']
    list_filter = ['department', 'position']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'department', 'position']
    raw_id_fields = ['user']
    
    fieldsets = (
        ('Пользователь', {'fields': ('user',)}),
        ('Рабочая информация', {
            'fields': ('department', 'position', 'experience_years')
        }),
        ('Дополнительно', {
            'fields': ('skills', 'interests'),
            'classes': ('collapse',)
        }),
    )
















