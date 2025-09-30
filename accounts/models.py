from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Упрощенная модель пользователя с ролями"""
    
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('editor', 'Редактор'),
        ('admin', 'Администратор'),
    ]
    
    # Поля для упрощенной регистрации (необязательные)
    first_name = models.CharField(max_length=30, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Фамилия')
    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    
    # Дополнительные поля (необязательные)
    email = models.EmailField(blank=True, verbose_name='Email')
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='user',
        verbose_name='Роль'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name='Аватар'
    )
    bio = models.TextField(blank=True, verbose_name='О себе')
    is_verified = models.BooleanField(default=False, verbose_name='Подтвержден')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} (@{self.username})"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_editor(self):
        return self.role in ['editor', 'admin']
    
    @property
    def can_moderate(self):
        return self.role in ['editor', 'admin']
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class UserProfile(models.Model):
    """Дополнительный профиль пользователя"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='Пользователь'
    )
    department = models.CharField(max_length=100, blank=True, verbose_name='Отдел')
    position = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    experience_years = models.PositiveIntegerField(default=0, verbose_name='Опыт работы (лет)')
    skills = models.TextField(blank=True, verbose_name='Навыки')
    interests = models.TextField(blank=True, verbose_name='Интересы')
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f"Профиль {self.user.get_full_name()}"
















