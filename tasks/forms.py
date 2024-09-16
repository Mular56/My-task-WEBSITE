from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assignee']
        widgets = {
            'status': forms.Select(choices=Task.STATUS_CHOICES),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user is None:
            return
        
        if not user.is_superuser:
            self.fields['assignee'].initial = user
            self.fields['assignee'].widget = forms.HiddenInput() 
        else:
            self.fields['assignee'].queryset = User.objects.all()
