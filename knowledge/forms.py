from django import forms
from .models import Article, Comment, Category, ArticleScreenshot, ArticleAttachment
from accounts.models import User
from .widgets import ProseMirrorWidget


class ArticleForm(forms.ModelForm):
    """Форма для создания/редактирования статьи"""
    
    # Добавляем поле для выбора типа публикации
    publication_type = forms.ChoiceField(
        choices=[
            ('publish', 'Опубликовать сразу'),
            ('draft', 'Сохранить как черновик'),
            ('suggestion', 'Отправить на модерацию'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='suggestion',
        label='Тип публикации'
    )

    class Meta:
        model = Article
        fields = ['title', 'slug', 'category', 'excerpt', 'content', 'tags', 'is_featured', 'allow_comments']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок статьи'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL статьи (будет сгенерирован автоматически)'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control excerpt-field',
                'rows': 5,
                'placeholder': 'Краткое описание статьи для превью (до 500 символов)',
                'maxlength': '500'
            }),
            'content': ProseMirrorWidget(),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Теги через запятую'
            }),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'allow_comments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        # Делаем slug необязательным для создания
        self.fields['slug'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        # Убираем генерацию slug из формы - это делается в представлении
        return cleaned_data


class CommentForm(forms.ModelForm):
    """Форма для добавления комментария"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ваш комментарий...'
            }),
        }


class SearchForm(forms.Form):
    """Форма поиска"""
    
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по базе знаний...',
            'autocomplete': 'off'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="Все категории",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)


class CategoryForm(forms.ModelForm):
    """Форма для создания/редактирования категории"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'color', 'is_active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название категории'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание категории'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CSS класс иконки (например: fas fa-book)'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ScreenshotForm(forms.ModelForm):
    """Форма для добавления скриншотов к статье"""
    
    class Meta:
        model = ArticleScreenshot
        fields = ['image', 'title', 'description', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название скриншота'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание скриншота'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }


class AttachmentForm(forms.ModelForm):
    """Форма для загрузки вложений к статье"""
    
    class Meta:
        model = ArticleAttachment
        fields = ['file', 'file_type', 'description']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.txt,.csv,.pdf,.doc,.docx,.jpg,.jpeg,.png,.gif,.bmp,.svg'
            }),
            'file_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание файла (необязательно)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле file_type из обязательных, будем определять автоматически
        self.fields['file_type'].required = False
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Ограничиваем размер файла (10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 10MB')
            
            # Определяем тип файла по расширению
            file_name = file.name.lower()
            if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg')):
                self.cleaned_data['file_type'] = 'image'
            elif file_name.endswith('.csv'):
                self.cleaned_data['file_type'] = 'csv'
            elif file_name.endswith(('.txt', '.md')):
                self.cleaned_data['file_type'] = 'text'
            elif file_name.endswith(('.pdf', '.doc', '.docx')):
                self.cleaned_data['file_type'] = 'document'
            else:
                self.cleaned_data['file_type'] = 'other'
        
        return file


class UserManagementForm(forms.ModelForm):
    """Форма для управления пользователями (только для админов)"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('user', 'Пользователь'),
                ('editor', 'Редактор'),
                ('admin', 'Администратор'),
            ]),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
















