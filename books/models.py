from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
import os

User = get_user_model()


class Category(models.Model):
    """Категории книг"""
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('URL', max_length=100, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Теги для книг"""
    name = models.CharField('Название', max_length=50, unique=True)
    color = models.CharField('Цвет', max_length=7, default='#007bff', 
                           help_text='HEX цвет (например: #007bff)')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги"""
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True, blank=True)
    author = models.CharField('Автор', max_length=200)
    description = models.TextField('Описание', blank=True)
    cover_image = models.ImageField('Обложка', upload_to='books/covers/', 
                                  blank=True, null=True)
    pdf_file = models.FileField('PDF файл', upload_to='books/pdfs/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                               verbose_name='Категория', related_name='books')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги', 
                                related_name='books')
    is_published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'slug': self.slug})
    
    def get_pdf_url(self):
        """Возвращает URL для чтения PDF"""
        return reverse('books:book_read', kwargs={'slug': self.slug})
    
    def get_file_size(self):
        """Возвращает размер файла в удобном формате"""
        if self.pdf_file:
            size = self.pdf_file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        return "Неизвестно"
    
    def get_file_extension(self):
        """Возвращает расширение файла"""
        if self.pdf_file:
            return os.path.splitext(self.pdf_file.name)[1].lower()
        return ""


class BookView(models.Model):
    """Модель для отслеживания просмотров книг"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, 
                           verbose_name='Книга', related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                           verbose_name='Пользователь', null=True, blank=True)
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)
    viewed_at = models.DateTimeField('Дата просмотра', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Просмотр книги'
        verbose_name_plural = 'Просмотры книг'
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.book.title} - {self.viewed_at}"

