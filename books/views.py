from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.http import Http404, FileResponse
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView
from .models import Book, Category, Tag, BookView
from .forms import BookSearchForm, BookFilterForm


class BookListView(ListView):
    """Список всех книг"""
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Book.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
        
        # Поиск
        search_query = self.request.GET.get('query')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Фильтр по категории
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Фильтр по тегам
        tag_ids = self.request.GET.getlist('tags')
        if tag_ids:
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()
        
        # Сортировка
        sort_by = self.request.GET.get('sort_by', '-created_at')
        queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = BookSearchForm(self.request.GET)
        context['filter_form'] = BookFilterForm(self.request.GET)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class BookDetailView(DetailView):
    """Детальная страница книги"""
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Book.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        
        # Похожие книги
        similar_books = Book.objects.filter(
            category=book.category,
            is_published=True
        ).exclude(id=book.id)[:4]
        
        context['similar_books'] = similar_books
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        
        # Записываем просмотр
        book = self.get_object()
        BookView.objects.create(
            book=book,
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response


def book_read(request, slug):
    """Страница для чтения PDF книги"""
    book = get_object_or_404(Book, slug=slug, is_published=True)
    
    # Проверяем, что файл существует
    if not book.pdf_file:
        raise Http404("Файл книги не найден")
    
    context = {
        'book': book,
    }
    
    return render(request, 'books/book_read.html', context)


def book_download(request, slug):
    """Скачивание PDF файла книги"""
    book = get_object_or_404(Book, slug=slug, is_published=True)
    
    if not book.pdf_file:
        raise Http404("Файл книги не найден")
    
    # Записываем скачивание как просмотр
    BookView.objects.create(
        book=book,
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    response = FileResponse(
        book.pdf_file.open('rb'),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
    return response


def category_books(request, slug):
    """Книги определенной категории"""
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(
        category=category, 
        is_published=True
    ).select_related('category').prefetch_related('tags')
    
    # Поиск в рамках категории
    search_query = request.GET.get('query')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Сортировка
    sort_by = request.GET.get('sort_by', '-created_at')
    books = books.order_by(sort_by)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'books': page_obj,
        'search_form': BookSearchForm(request.GET),
        'filter_form': BookFilterForm(request.GET),
    }
    
    return render(request, 'books/category_books.html', context)


def tag_books(request, slug):
    """Книги с определенным тегом"""
    tag = get_object_or_404(Tag, slug=slug)
    books = Book.objects.filter(
        tags=tag, 
        is_published=True
    ).select_related('category').prefetch_related('tags').distinct()
    
    # Поиск в рамках тега
    search_query = request.GET.get('query')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Сортировка
    sort_by = request.GET.get('sort_by', '-created_at')
    books = books.order_by(sort_by)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'books': page_obj,
        'search_form': BookSearchForm(request.GET),
        'filter_form': BookFilterForm(request.GET),
    }
    
    return render(request, 'books/tag_books.html', context)


class BookCreateView(CreateView):
    """Создание новой книги"""
    model = Book
    fields = ['title', 'author', 'description', 'category', 'tags', 'pdf_file']
    template_name = 'books/book_add.html'
    success_url = reverse_lazy('books:book_list')
    
    def form_valid(self, form):
        # Автоматически генерируем slug
        from django.utils.text import slugify
        form.instance.slug = slugify(form.instance.title)
        form.instance.is_published = True
        messages.success(self.request, 'Книга успешно добавлена!')
        return super().form_valid(form)
