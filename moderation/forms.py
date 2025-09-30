from django import forms
from .models import ContentSuggestion
from knowledge.models import Category, Article


class ContentSuggestionForm(forms.ModelForm):
    """Форма для создания предложений контента"""
    
    class Meta:
        model = ContentSuggestion
        fields = [
            'title', 'content', 'suggestion_type', 'category', 
            'target_article', 'tags', 'priority'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Введите содержание'
            }),
            'suggestion_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'target_article': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите теги через запятую'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ограничиваем выбор категорий только активными
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        
        # Ограничиваем выбор статей только опубликованными
        self.fields['target_article'].queryset = Article.objects.filter(status='published')
        
        # Делаем поля необязательными в зависимости от типа предложения
        if 'suggestion_type' in self.data:
            suggestion_type = self.data['suggestion_type']
            if suggestion_type == 'article':
                self.fields['target_article'].required = False
            elif suggestion_type == 'edit':
                self.fields['category'].required = False
                self.fields['target_article'].required = True
            elif suggestion_type in ['category', 'tag']:
                self.fields['target_article'].required = False
                self.fields['category'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        suggestion_type = cleaned_data.get('suggestion_type')
        category = cleaned_data.get('category')
        target_article = cleaned_data.get('target_article')
        
        # Валидация в зависимости от типа предложения
        if suggestion_type == 'article' and not category:
            raise forms.ValidationError('Для предложения новой статьи необходимо выбрать категорию.')
        
        if suggestion_type == 'edit' and not target_article:
            raise forms.ValidationError('Для предложения редактирования необходимо выбрать статью.')
        
        return cleaned_data
