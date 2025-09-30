from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import uuid
from PIL import Image
from .models import Category, Article, Comment, ArticleView, Favorite, ArticleAttachment
from .forms import ArticleForm, CommentForm, SearchForm, AttachmentForm, CategoryForm

User = get_user_model()


def home_view(request):
    """Главная страница"""
    featured_articles = Article.objects.filter(
        status='published', 
        is_featured=True,
        slug__isnull=False
    ).exclude(slug='').order_by('-created_at')[:6]
    
    recent_articles = Article.objects.filter(
        status='published',
        slug__isnull=False
    ).exclude(slug='').order_by('-created_at')[:10]
    
    categories = Category.objects.filter(is_active=True).annotate(
        articles_count=Count('articles', filter=Q(articles__status='published'))
    ).order_by('order', 'name')
    
    context = {
        'featured_articles': featured_articles,
        'recent_articles': recent_articles,
        'categories': categories,
    }
    return render(request, 'knowledge/home.html', context)


def category_list_view(request):
    """Список всех категорий"""
    categories = Category.objects.filter(is_active=True).annotate(
        articles_count=Count('articles', filter=Q(articles__status='published'))
    ).order_by('order', 'name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'knowledge/category_list.html', context)


def category_detail_view(request, slug):
    """Детальная страница категории"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    articles = Article.objects.filter(
        category=category, 
        status='published'
    ).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'articles': page_obj,
    }
    return render(request, 'knowledge/category_detail.html', context)


def article_detail_view(request, slug):
    """Детальная страница статьи"""
    # Разрешаем просмотр статей в зависимости от статуса и роли пользователя
    if request.user.is_authenticated:
        if request.user.can_moderate or request.user.is_staff:
            # Модераторы и админы видят все статьи
            article = get_object_or_404(Article, slug=slug)
        else:
            # Обычные пользователи видят только опубликованные статьи и свои статьи
            try:
                article = get_object_or_404(Article, slug=slug, status='published')
            except:
                # Если не найдена опубликованная статья, проверяем, является ли пользователь автором
                article = get_object_or_404(Article, slug=slug, author=request.user)
    else:
        # Неавторизованные пользователи видят только опубликованные статьи
        article = get_object_or_404(Article, slug=slug, status='published')
    
    # Увеличиваем счетчик просмотров
    article.increment_views()
    
    # Записываем просмотр
    try:
        if request.user.is_authenticated:
            ArticleView.objects.get_or_create(
                article=article,
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR'),
                defaults={
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                }
            )
        else:
            ArticleView.objects.get_or_create(
                article=article,
                user=None,
                ip_address=request.META.get('REMOTE_ADDR'),
                defaults={
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                }
            )
    except Exception as e:
        # Игнорируем ошибки при записи просмотров
        print(f"Ошибка записи просмотра: {e}")
        pass
    
    # Получаем комментарии
    comments = Comment.objects.filter(
        article=article, 
        is_approved=True,
        parent=None
    ).order_by('-created_at')
    
    # Форма для добавления комментария
    comment_form = CommentForm()
    
    # Проверяем, добавлена ли статья в избранное
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user, 
            article=article
        ).exists()
    
    # Похожие статьи
    similar_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id).order_by('-views_count')[:4]
    
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'is_favorite': is_favorite,
        'similar_articles': similar_articles,
    }
    return render(request, 'knowledge/article_detail.html', context)


def search_view(request):
    """Поиск по базе знаний"""
    form = SearchForm(request.GET)
    articles = Article.objects.none()
    
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            articles = Article.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__icontains=query) |
                Q(excerpt__icontains=query),
                status='published'
            ).order_by('-views_count', '-created_at')
    
    # Пагинация
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'articles': page_obj,
        'query': request.GET.get('query', ''),
    }
    return render(request, 'knowledge/search.html', context)


@login_required
@require_POST
def add_comment(request, article_slug):
    """Добавление комментария к статье"""
    # Разрешаем комментарии к черновикам для авторов и редакторов
    if request.user.is_authenticated and (request.user.is_editor or request.user.is_staff):
        article = get_object_or_404(Article, slug=article_slug)
    else:
        article = get_object_or_404(Article, slug=article_slug, status='published')
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        
        # Обработка ответа на комментарий
        parent_id = request.POST.get('parent_id')
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id, article=article)
                comment.parent = parent_comment
            except Comment.DoesNotExist:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Родительский комментарий не найден.'})
                messages.error(request, 'Родительский комментарий не найден.')
                return redirect('knowledge:article_detail', slug=article.slug)
        
        comment.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if parent_id:
                return JsonResponse({'success': True, 'message': 'Ответ добавлен и будет опубликован после модерации.'})
            else:
                return JsonResponse({'success': True, 'message': 'Комментарий добавлен и будет опубликован после модерации.'})
        
        if parent_id:
            messages.success(request, 'Ответ добавлен и будет опубликован после модерации.')
        else:
            messages.success(request, 'Комментарий добавлен и будет опубликован после модерации.')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Ошибка при добавлении комментария.'})
        messages.error(request, 'Ошибка при добавлении комментария.')
    
    return redirect('knowledge:article_detail', slug=article_slug)


@login_required
@require_POST
def toggle_favorite(request, article_slug):
    """Добавление/удаление статьи из избранного"""
    # Разрешаем добавление в избранное черновиков для авторов и редакторов
    if request.user.is_authenticated and (request.user.is_editor or request.user.is_staff):
        article = get_object_or_404(Article, slug=article_slug)
    else:
        article = get_object_or_404(Article, slug=article_slug, status='published')
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        article=article
    )
    
    if not created:
        favorite.delete()
        action = 'removed'
    else:
        action = 'added'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'action': action,
            'is_favorite': created
        })
    
    return redirect('knowledge:article_detail', slug=article_slug)


@login_required
def my_favorites_view(request):
    """Избранные статьи пользователя"""
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'favorites': page_obj,
    }
    return render(request, 'knowledge/my_favorites.html', context)


@login_required
def my_articles_view(request):
    """Мои статьи и черновики"""
    # Получаем все статьи пользователя
    articles = Article.objects.filter(author=request.user).order_by('-created_at')
    
    # Фильтрация по статусу
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        articles = articles.filter(status=status_filter)
    
    # Пагинация
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Статистика
    stats = {
        'total': Article.objects.filter(author=request.user).count(),
        'published': Article.objects.filter(author=request.user, status='published').count(),
        'draft': Article.objects.filter(author=request.user, status='draft').count(),
        'pending': Article.objects.filter(author=request.user, status='pending').count(),
    }
    
    context = {
        'page_obj': page_obj,
        'articles': page_obj,
        'status_filter': status_filter,
        'stats': stats,
    }
    return render(request, 'knowledge/my_articles.html', context)


@login_required
def create_article_view(request):
    """Создание новой статьи (для всех авторизованных пользователей)"""
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            
            # Получаем тип публикации из формы
            publication_type = form.cleaned_data.get('publication_type', 'suggestion')
            
            # Устанавливаем статус в зависимости от типа публикации
            if publication_type == 'publish':
                # Только редакторы и админы могут публиковать сразу
                if request.user.is_editor or request.user.is_admin:
                    article.status = 'published'
                else:
                    article.status = 'pending'
                    publication_type = 'suggestion'
            elif publication_type == 'draft':
                article.status = 'draft'
            else:  # suggestion
                article.status = 'pending'
            
            # Генерируем slug если он не указан
            if not article.slug:
                from .utils import slugify_cyrillic, create_unique_slug
                article.slug = create_unique_slug(Article, slugify_cyrillic(article.title))
            else:
                from .utils import slugify_cyrillic, create_unique_slug
                article.slug = create_unique_slug(Article, slugify_cyrillic(article.slug), article)
            
            try:
                article.save()
                
                if publication_type == 'suggestion' or article.status == 'pending':
                    # Создаем уведомление для модераторов
                    from moderation.models import Notification
                    moderators = User.objects.filter(role__in=['editor', 'admin']).exclude(id=article.author.id)
                    
                    for moderator in moderators:
                        Notification.objects.create(
                            user=moderator,
                            title='Новая статья на рассмотрении',
                            message=f'Пользователь {article.author.get_full_name()} создал новую статью "{article.title}" и отправил её на рассмотрение.',
                            notification_type='moderation_required'
                        )
                    
                    messages.success(request, f'Статья "{article.title}" создана и отправлена на рассмотрение. Модераторы будут уведомлены.')
                    return redirect('moderation:suggestion_list')
                elif publication_type == 'draft':
                    messages.success(request, f'Статья "{article.title}" сохранена как черновик.')
                    return redirect('knowledge:my_articles')
                else:
                    # Для черновиков
                    messages.success(request, f'Статья "{article.title}" сохранена в черновик. Вы можете продолжить редактирование позже.')
                    print(f"✅ Сообщение о черновике добавлено")
                    return redirect('knowledge:home')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении статьи: {str(e)}')
                print(f"❌ Ошибка сохранения: {e}")
                import traceback
                traceback.print_exc()
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            print(f"❌ Ошибки формы: {form.errors}")
            for field, errors in form.errors.items():
                print(f"   {field}: {errors}")
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
    }
    return render(request, 'knowledge/create_article.html', context)


@login_required
def create_category_view(request):
    """Создание новой категории (для всех авторизованных пользователей)"""
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            # Генерируем slug если он не указан
            if not category.slug:
                from .utils import slugify_cyrillic, create_unique_slug
                category.slug = create_unique_slug(Category, slugify_cyrillic(category.name))
            else:
                from .utils import slugify_cyrillic, create_unique_slug
                category.slug = create_unique_slug(Category, slugify_cyrillic(category.slug), category)
            
            try:
                category.save()
                messages.success(request, f'Категория "{category.name}" создана.')
                return redirect('knowledge:category_detail', slug=category.slug)
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении категории: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
    }
    return render(request, 'knowledge/create_category.html', context)


@login_required
def upload_attachment_view(request, slug):
    """Загрузка вложения к статье"""
    article = get_object_or_404(Article, slug=slug)
    
    if request.user != article.author:
        messages.error(request, 'Только автор статьи может добавлять файлы.')
        return redirect('knowledge:article_detail', slug=slug)
    
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.article = article
            attachment.uploaded_by = request.user
            attachment.original_name = attachment.file.name
            
            # Определяем тип файла автоматически
            file_name = attachment.file.name.lower()
            if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg')):
                attachment.file_type = 'image'
            elif file_name.endswith('.csv'):
                attachment.file_type = 'csv'
            elif file_name.endswith(('.txt', '.md')):
                attachment.file_type = 'text'
            elif file_name.endswith(('.pdf', '.doc', '.docx')):
                attachment.file_type = 'document'
            else:
                attachment.file_type = 'other'
            
            try:
                attachment.save()
                messages.success(request, f'Файл "{attachment.original_name}" загружен.')
            except Exception as e:
                messages.error(request, f'Ошибка при загрузке файла: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    
    return redirect('knowledge:article_detail', slug=slug)


def download_attachment_view(request, attachment_id):
    """Скачивание вложения"""
    attachment = get_object_or_404(ArticleAttachment, id=attachment_id)
    
    # Увеличиваем счетчик скачиваний
    attachment.increment_downloads()
    
    # Возвращаем файл для скачивания
    from django.http import FileResponse
    response = FileResponse(attachment.file, as_attachment=True, filename=attachment.original_name)
    return response


@login_required
@require_POST
def upload_image_view(request):
    """Загрузка изображения для вставки в статью (как в Word)"""
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'Файл изображения не найден'}, status=400)
        
        image_file = request.FILES['image']
        
        # Проверяем тип файла
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if image_file.content_type not in allowed_types:
            return JsonResponse({'error': 'Неподдерживаемый тип файла. Разрешены: JPEG, PNG, GIF, WebP'}, status=400)
        
        # Проверяем размер файла (максимум 10MB)
        if image_file.size > 10 * 1024 * 1024:
            return JsonResponse({'error': 'Файл слишком большой. Максимальный размер: 10MB'}, status=400)
        
        # Создаем уникальное имя файла
        file_extension = os.path.splitext(image_file.name)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Путь для сохранения
        upload_path = f"article_images/{unique_filename}"
        
        # Сохраняем файл
        file_path = default_storage.save(upload_path, ContentFile(image_file.read()))
        
        # Получаем URL файла
        file_url = default_storage.url(file_path)
        
        # Получаем параметры выравнивания
        alignment = request.POST.get('alignment', 'center')
        
        # Генерируем HTML для вставки
        image_html = generate_image_html(file_url, image_file.name, alignment)
        
        return JsonResponse({
            'success': True,
            'url': file_url,
            'html': image_html,
            'filename': image_file.name
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Ошибка при загрузке изображения: {str(e)}'}, status=500)


def generate_image_html(image_url, filename, alignment='center'):
    """Генерирует HTML для изображения в зависимости от выравнивания"""
    # Извлекаем имя файла без расширения для alt текста
    alt_text = os.path.splitext(filename)[0]
    
    if alignment == 'left':
        return f'''<div class="image-container float-start">
    <img src="{image_url}" alt="{alt_text}" class="img-fluid">
    <div class="image-caption">{alt_text}</div>
</div>'''
    elif alignment == 'right':
        return f'''<div class="image-container float-end">
    <img src="{image_url}" alt="{alt_text}" class="img-fluid">
    <div class="image-caption">{alt_text}</div>
</div>'''
    elif alignment == 'full':
        return f'''<div class="image-container full-width">
    <img src="{image_url}" alt="{alt_text}" class="img-fluid">
    <div class="image-caption">{alt_text}</div>
</div>'''
    else:  # center
        return f'''<div class="image-container">
    <img src="{image_url}" alt="{alt_text}" class="img-fluid">
    <div class="image-caption">{alt_text}</div>
</div>'''
















