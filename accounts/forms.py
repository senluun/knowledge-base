from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Упрощенная форма регистрации пользователя - только username и пароль"""
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Введите имя пользователя (можно как имя или фамилию)'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Введите пароль (минимум 6 символов)'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Подтвердите пароль'
        })
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise ValidationError('Пароль должен содержать минимум 6 символов.')
        return password1
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Устанавливаем имя пользователя как first_name и last_name
        user.first_name = self.cleaned_data['username']
        user.last_name = ''
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Форма обновления профиля пользователя"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    """Форма профиля пользователя"""
    
    class Meta:
        model = UserProfile
        fields = ['department', 'position', 'experience_years', 'skills', 'interests']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LoginForm(forms.Form):
    """Упрощенная форма входа"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
















