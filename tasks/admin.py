from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'creator', 'assignee', 'created_at', 'updated_at')
    list_filter = ('status', 'creator', 'assignee')
    search_fields = ('title', 'description')
