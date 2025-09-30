from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import ContentSuggestion, ModerationLog, Notification
from .forms import ContentSuggestionForm
from knowledge.models import Article, Category


@login_required
def moderation_dashboard(request):
    """Дашборд модерации"""
    if not request.user.is_editor:
        messages.error(request, 'У вас нет прав для доступа к панели модерации.')
        return redirect('knowledge:home')
    
    # Статистика для модераторов (статьи на модерации)
    pending_articles = Article.objects.filter(status='pending').count()
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(status='published').count()
    
    # Последние статьи на модерации
    recent_articles = Article.objects.filter(
        status='pending'
    ).order_by('-created_at')[:5]
    
    context = {
        'pending_articles': pending_articles,
        'total_articles': total_articles,
        'published_articles': published_articles,
        'recent_articles': recent_articles,
    }
    return render(request, 'moderation/dashboard.html', context)


@login_required
def suggestion_list(request):
    """Список предложений для модерации"""
    if not request.user.is_editor:
        messages.error(request, 'У вас нет прав для просмотра предложений.')
        return redirect('knowledge:home')
    
    status_filter = request.GET.get('status', 'pending')
    
    # Получаем статьи со статусом pending для модерации
    from knowledge.models import Article
    suggestions = Article.objects.filter(status='pending')
    
    if status_filter:
        suggestions = suggestions.filter(status=status_filter)
    
    suggestions = suggestions.order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(suggestions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'suggestions': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'moderation/suggestion_list.html', context)


@login_required
def suggestion_detail(request, pk):
    """Детальная страница предложения"""
    if not request.user.is_editor:
        messages.error(request, 'У вас нет прав для просмотра предложений.')
        return redirect('knowledge:home')
    
    suggestion = get_object_or_404(ContentSuggestion, pk=pk)
    
    # Лог модерации
    moderation_logs = ModerationLog.objects.filter(suggestion=suggestion).order_by('-created_at')
    
    context = {
        'suggestion': suggestion,
        'moderation_logs': moderation_logs,
    }
    return render(request, 'moderation/suggestion_detail.html', context)


@login_required
@require_POST
def approve_suggestion(request, pk):
    """Одобрение предложения"""
    if not request.user.is_editor:
        return JsonResponse({'error': 'Нет прав для модерации'}, status=403)
    
    suggestion = get_object_or_404(ContentSuggestion, pk=pk)
    
    if suggestion.status != 'pending':
        return JsonResponse({'error': 'Предложение уже обработано'}, status=400)
    
    # Одобряем предложение
    suggestion.status = 'approved'
    suggestion.moderator = request.user
    suggestion.moderated_at = timezone.now()
    suggestion.save()
    
    # Создаем лог
    ModerationLog.objects.create(
        suggestion=suggestion,
        moderator=request.user,
        action='approve',
        comment=request.POST.get('comment', '')
    )
    
    # Создаем уведомление для автора
    Notification.objects.create(
        user=suggestion.author,
        notification_type='suggestion_approved',
        title='Предложение одобрено',
        message=f'Ваше предложение "{suggestion.title}" было одобрено модератором.',
        content_object=suggestion
    )
    
    # Если это предложение новой статьи, создаем статью
    if suggestion.suggestion_type == 'article':
        from django.utils.text import slugify
        from django.utils import timezone
        
        slug = slugify(suggestion.title)
        # Делаем slug уникальным
        counter = 1
        original_slug = slug
        while Article.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
            
        article = Article.objects.create(
            title=suggestion.title,
            slug=slug,
            content=suggestion.content,
            category=suggestion.category,
            author=suggestion.author,
            status='published',
            tags=suggestion.tags
        )
        messages.success(request, f'Статья "{article.title}" создана и опубликована.')
    
    messages.success(request, 'Предложение одобрено.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'approved'})
    
    return redirect('moderation:suggestion_detail', pk=pk)


@login_required
@require_POST
def reject_suggestion(request, pk):
    """Отклонение предложения"""
    if not request.user.is_editor:
        return JsonResponse({'error': 'Нет прав для модерации'}, status=403)
    
    suggestion = get_object_or_404(ContentSuggestion, pk=pk)
    
    if suggestion.status != 'pending':
        return JsonResponse({'error': 'Предложение уже обработано'}, status=400)
    
    comment = request.POST.get('comment', '')
    if not comment:
        messages.error(request, 'Необходимо указать причину отклонения.')
        return redirect('moderation:suggestion_detail', pk=pk)
    
    # Отклоняем предложение
    suggestion.status = 'rejected'
    suggestion.moderator = request.user
    suggestion.moderator_comment = comment
    suggestion.moderated_at = timezone.now()
    suggestion.save()
    
    # Создаем лог
    ModerationLog.objects.create(
        suggestion=suggestion,
        moderator=request.user,
        action='reject',
        comment=comment
    )
    
    # Создаем уведомление для автора
    Notification.objects.create(
        user=suggestion.author,
        notification_type='suggestion_rejected',
        title='Предложение отклонено',
        message=f'Ваше предложение "{suggestion.title}" было отклонено. Причина: {comment}',
        content_object=suggestion
    )
    
    messages.success(request, 'Предложение отклонено.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'rejected'})
    
    return redirect('moderation:suggestion_detail', pk=pk)


@login_required
@require_POST
def request_revision(request, pk):
    """Запрос доработки предложения"""
    if not request.user.is_editor:
        return JsonResponse({'error': 'Нет прав для модерации'}, status=403)
    
    suggestion = get_object_or_404(ContentSuggestion, pk=pk)
    
    if suggestion.status != 'pending':
        return JsonResponse({'error': 'Предложение уже обработано'}, status=400)
    
    comment = request.POST.get('comment', '')
    if not comment:
        messages.error(request, 'Необходимо указать, что нужно доработать.')
        return redirect('moderation:suggestion_detail', pk=pk)
    
    # Запрашиваем доработку
    suggestion.status = 'needs_revision'
    suggestion.moderator = request.user
    suggestion.moderator_comment = comment
    suggestion.moderated_at = timezone.now()
    suggestion.save()
    
    # Создаем лог
    ModerationLog.objects.create(
        suggestion=suggestion,
        moderator=request.user,
        action='request_revision',
        comment=comment
    )
    
    # Создаем уведомление для автора
    Notification.objects.create(
        user=suggestion.author,
        notification_type='suggestion_revision',
        title='Требуется доработка',
        message=f'Ваше предложение "{suggestion.title}" требует доработки. Комментарий: {comment}',
        content_object=suggestion
    )
    
    messages.success(request, 'Запрошена доработка предложения.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'needs_revision'})
    
    return redirect('moderation:suggestion_detail', pk=pk)


@login_required
def create_suggestion(request):
    """Создание нового предложения"""
    if request.method == 'POST':
        form = ContentSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.author = request.user
            suggestion.save()
            
            messages.success(request, 'Предложение отправлено на модерацию.')
            return redirect('moderation:my_suggestions')
    else:
        form = ContentSuggestionForm()
    
    context = {
        'form': form,
    }
    return render(request, 'moderation/create_suggestion.html', context)


@login_required
def my_suggestions(request):
    """Мои предложения"""
    suggestions = ContentSuggestion.objects.filter(
        author=request.user
    ).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(suggestions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'suggestions': page_obj,
    }
    return render(request, 'moderation/my_suggestions.html', context)


@login_required
def mark_all_notifications_read(request):
    """Отметить все уведомления как прочитанные"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'Все уведомления отмечены как прочитанные.')
    return redirect('moderation:notifications')


@login_required
def notifications(request):
    """Уведомления пользователя"""
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'notifications': page_obj,
    }
    return render(request, 'moderation/notifications.html', context)


@login_required
@require_POST
def mark_notification_read(request, pk):
    """Отметить уведомление как прочитанное"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'read'})
    
    return redirect('moderation:notifications')

















