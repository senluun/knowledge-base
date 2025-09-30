from django.contrib import admin
from .models import Category, Tag, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at')
    list_filter = ('category', 'tags', 'is_published', 'created_at')
    search_fields = ('title', 'author', 'description')
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'author', 'description', 'cover_image')
        }),
        ('Классификация', {
            'fields': ('category', 'tags')
        }),
        ('Файл книги', {
            'fields': ('pdf_file',)
        }),
        ('Публикация', {
            'fields': ('is_published',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

