"""
URL configuration for knowledge_base project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('knowledge:home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('knowledge/', include('knowledge.urls')),
    path('moderation/', include('moderation.urls')),
    path('books/', include('books.urls')),
    path('', home_redirect, name='home'),  # Редирект на главную страницу
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)















