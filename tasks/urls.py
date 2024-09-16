from django.urls import path
from .views import HomePageView, TaskCreateView, TaskUpdateView, move_task, TaskByStatusView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    
    path('task/create/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/move/<str:status>/', move_task, name='move_task'),
    
    path('tasks/status/<str:status>/', TaskByStatusView.as_view(), name='tasks-by-status'),
]