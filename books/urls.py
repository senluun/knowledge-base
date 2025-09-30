from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<slug:slug>/read/', views.book_read, name='book_read'),
    path('book/<slug:slug>/download/', views.book_download, name='book_download'),
    path('category/<slug:slug>/', views.category_books, name='category_books'),
    path('tag/<slug:slug>/', views.tag_books, name='tag_books'),
    path('add/', views.BookCreateView.as_view(), name='book_add'),
]
