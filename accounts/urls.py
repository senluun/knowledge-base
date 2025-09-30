from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:user_id>/toggle-status/', views.user_toggle_status, name='user_toggle_status'),
    path('users/<int:user_id>/change-role/', views.user_change_role, name='user_change_role'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('search/', views.user_search_view, name='user_search'),
    path('profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
]
















