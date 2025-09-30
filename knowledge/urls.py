from django.urls import path, re_path
from . import views

app_name = 'knowledge'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('categories/', views.category_list_view, name='category_list'),
    re_path(r'^category/(?P<slug>[\w\-]+)/$', views.category_detail_view, name='category_detail'),
    re_path(r'^article/(?P<slug>[\w\-]+)/$', views.article_detail_view, name='article_detail'),
    path('search/', views.search_view, name='search'),
    path('favorites/', views.my_favorites_view, name='my_favorites'),
    path('my-articles/', views.my_articles_view, name='my_articles'),
    path('create-article/', views.create_article_view, name='create_article'),
    path('create-category/', views.create_category_view, name='create_category'),
    re_path(r'^article/(?P<article_slug>[\w\-]+)/comment/$', views.add_comment, name='add_comment'),
    re_path(r'^article/(?P<article_slug>[\w\-]+)/favorite/$', views.toggle_favorite, name='toggle_favorite'),
    re_path(r'^article/(?P<slug>[\w\-]+)/upload/$', views.upload_attachment_view, name='upload_attachment'),
    path('attachment/<int:attachment_id>/download/', views.download_attachment_view, name='download_attachment'),
    path('upload-image/', views.upload_image_view, name='upload_image'),
]
















