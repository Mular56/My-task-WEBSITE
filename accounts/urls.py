from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  
from .views import CustomLogoutView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  
    path('dashboard/', views.dashboard, name='dashboard'),
    path('non_authenticated/', views.non_authenticated_view, name='non_authenticated'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
