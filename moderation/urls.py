from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('', views.moderation_dashboard, name='dashboard'),
    path('suggestions/', views.suggestion_list, name='suggestion_list'),
    path('suggestions/<int:pk>/', views.suggestion_detail, name='suggestion_detail'),
    path('suggestions/<int:pk>/approve/', views.approve_suggestion, name='approve_suggestion'),
    path('suggestions/<int:pk>/reject/', views.reject_suggestion, name='reject_suggestion'),
    path('suggestions/<int:pk>/request-revision/', views.request_revision, name='request_revision'),
    # path('create-suggestion/', views.create_suggestion, name='create_suggestion'),  # Объединено с созданием статьи
    path('my-suggestions/', views.my_suggestions, name='my_suggestions'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_read'),
]
















