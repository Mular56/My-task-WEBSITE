from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()  
    assignee = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'creator', 'assignee', 'updated_at']
