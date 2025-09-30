from django import forms
from .models import Book, Category, Tag


class BookSearchForm(forms.Form):
    """Форма поиска книг"""
    query = forms.CharField(
        label='Поиск',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название книги или автора...'
        })
    )
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
        required=False,
        empty_label='Все категории',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tags = forms.ModelMultipleChoiceField(
        label='Теги',
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )


class BookFilterForm(forms.Form):
    """Форма фильтрации книг"""
    SORT_CHOICES = [
        ('-created_at', 'Новые сначала'),
        ('created_at', 'Старые сначала'),
        ('title', 'По названию А-Я'),
        ('-title', 'По названию Я-А'),
        ('author', 'По автору А-Я'),
        ('-author', 'По автору Я-А'),
    ]
    
    sort_by = forms.ChoiceField(
        label='Сортировка',
        choices=SORT_CHOICES,
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
        required=False,
        empty_label='Все категории',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tags = forms.ModelMultipleChoiceField(
        label='Теги',
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

