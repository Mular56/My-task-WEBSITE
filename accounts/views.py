from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm
from tasks.models import Task


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


def non_authenticated_view(request):
    return render(request, 'non_authenticated.html')


@login_required
def profile_view(request):
    return render(request, 'profile.html')
    

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user) 
            return redirect('profile')  
        else:
            print(form.errors)  
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_superuser:
        tasks_by_status = {
            'new': Task.objects.filter(status='new'),
            'in_progress': Task.objects.filter(status='in_progress'),
            'in_qa': Task.objects.filter(status='in_qa'),
            'ready': Task.objects.filter(status='ready'),
            'done': Task.objects.filter(status='done'),
        }
    else:
        tasks_by_status = {
            'new': Task.objects.filter(status='new', creator=request.user) | Task.objects.filter(status='new', assignee=request.user),
            'in_progress': Task.objects.filter(status='in_progress', creator=request.user) | Task.objects.filter(status='in_progress', assignee=request.user),
            'in_qa': Task.objects.filter(status='in_qa', creator=request.user) | Task.objects.filter(status='in_qa', assignee=request.user),
            'ready': Task.objects.filter(status='ready', creator=request.user) | Task.objects.filter(status='ready', assignee=request.user),
            'done': Task.objects.filter(status='done', creator=request.user) | Task.objects.filter(status='done', assignee=request.user),
        }

    return render(request, 'dashboard.html', {'tasks_by_status': tasks_by_status})
