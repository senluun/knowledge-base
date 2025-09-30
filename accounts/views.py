from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CustomUserCreationForm, UserUpdateForm, UserProfileForm, LoginForm
from .models import User, UserProfile
from knowledge.forms import UserManagementForm


def login_view(request):
    """Упрощенное представление для входа пользователя"""
    if request.user.is_authenticated:
        return redirect('knowledge:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Аутентификация по username
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Сессия истекает при закрытии браузера
                messages.success(request, f'Добро пожаловать, {user.get_full_name()}!')
                return redirect('knowledge:home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Представление для выхода пользователя"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('accounts:login')


class RegisterView(CreateView):
    """Представление для регистрации пользователя"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Регистрация прошла успешно! Теперь вы можете войти в систему.'
        )
        return response


@login_required
def profile_view(request):
    """Представление профиля пользователя"""
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_view(request):
    """Дашборд пользователя"""
    user = request.user
    
    # Статистика для разных ролей
    context = {
        'user': user,
    }
    
    if user.is_admin:
        # Статистика для администратора
        context.update({
            'total_users': User.objects.count(),
            'pending_suggestions': 0,  # Будет добавлено в модуле модерации
            'total_articles': 0,  # Будет добавлено в модуле знаний
        })
    elif user.is_editor:
        # Статистика для редактора
        context.update({
            'pending_suggestions': 0,  # Будет добавлено в модуле модерации
            'my_articles': 0,  # Будет добавлено в модуле знаний
        })
    else:
        # Статистика для обычного пользователя
        context.update({
            'my_suggestions': 0,  # Будет добавлено в модуле модерации
            'favorite_articles': 0,  # Будет добавлено в модуле знаний
        })
    
    return render(request, 'accounts/dashboard.html', context)


def user_list_view(request):
    """Список пользователей (только для админов и редакторов)"""
    if not request.user.is_editor:
        messages.error(request, 'У вас нет прав для просмотра этого раздела.')
        return redirect('knowledge:home')
    
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users,
    }
    return render(request, 'accounts/user_list.html', context)


@login_required
def user_edit_view(request, user_id):
    """Редактирование пользователя (только для админов)"""
    if not request.user.is_admin:
        messages.error(request, 'У вас нет прав для редактирования пользователей.')
        return redirect('knowledge:home')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserManagementForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Пользователь {user.get_full_name()} обновлен.')
            return redirect('accounts:user_list')
    else:
        form = UserManagementForm(instance=user)
    
    context = {
        'form': form,
        'user_obj': user,
    }
    return render(request, 'accounts/user_edit.html', context)


@login_required
@require_POST
def user_toggle_status(request, user_id):
    """Переключение статуса пользователя (активен/заблокирован)"""
    if not request.user.is_admin:
        messages.error(request, 'У вас нет прав для изменения статуса пользователей.')
        return redirect('knowledge:home')
    
    user = get_object_or_404(User, id=user_id)
    
    # Нельзя заблокировать себя
    if user == request.user:
        messages.error(request, 'Вы не можете заблокировать себя.')
        return redirect('accounts:user_list')
    
    user.is_active = not user.is_active
    user.save()
    
    status = 'активирован' if user.is_active else 'заблокирован'
    messages.success(request, f'Пользователь {user.get_full_name()} {status}.')
    
    return redirect('accounts:user_list')


@login_required
@require_POST
def user_change_role(request, user_id):
    """Изменение роли пользователя"""
    if not request.user.is_admin:
        messages.error(request, 'У вас нет прав для изменения ролей пользователей.')
        return redirect('knowledge:home')
    
    user = get_object_or_404(User, id=user_id)
    new_role = request.POST.get('role')
    
    if new_role in ['user', 'editor', 'admin']:
        user.role = new_role
        user.save()
        
        role_names = {
            'user': 'Пользователь',
            'editor': 'Редактор', 
            'admin': 'Администратор'
        }
        
        messages.success(request, f'Роль пользователя {user.get_full_name()} изменена на {role_names[new_role]}.')
    else:
        messages.error(request, 'Неверная роль.')
    
    return redirect('accounts:user_list')


@login_required
@require_POST
def user_delete(request, user_id):
    """Удаление пользователя"""
    if not request.user.is_admin:
        messages.error(request, 'У вас нет прав для удаления пользователей.')
        return redirect('knowledge:home')
    
    user = get_object_or_404(User, id=user_id)
    
    # Нельзя удалить себя
    if user == request.user:
        messages.error(request, 'Вы не можете удалить себя.')
        return redirect('accounts:user_list')
    
    user_name = user.get_full_name()
    user.delete()
    
    messages.success(request, f'Пользователь {user_name} удален.')
    return redirect('accounts:user_list')


@login_required
def user_search_view(request):
    """Поиск пользователей"""
    query = request.GET.get('q', '')
    users = User.objects.none()
    
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).exclude(id=request.user.id).order_by('username')
    
    # Пагинация
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'users': page_obj,
    }
    return render(request, 'accounts/user_search.html', context)


@login_required
def user_profile_view(request, user_id):
    """Просмотр профиля другого пользователя"""
    user_obj = get_object_or_404(User, id=user_id)
    
    # Нельзя просматривать свой профиль через эту функцию
    if user_obj == request.user:
        return redirect('accounts:profile')
    
    try:
        profile = user_obj.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    context = {
        'user_obj': user_obj,
        'profile': profile,
    }
    return render(request, 'accounts/user_profile.html', context)
















