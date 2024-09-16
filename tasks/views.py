from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import TaskSerializer


class HomePageView(TemplateView):
    template_name = 'base.html'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'create_task.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        if not self.request.user.is_superuser:
            form.instance.assignee = self.request.user  
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_edit.html'
    context_object_name = 'task'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if not (request.user == task.creator or request.user == task.assignee or request.user.is_superuser):
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            if request.user.is_superuser and not task.assignee:
                task.assignee = task.creator
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'create_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if not (request.user == task.creator or request.user == task.assignee or request.user.is_superuser):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task, user=request.user)
    
    return render(request, 'edit_task.html', {'form': form})


@login_required
def move_task(request, pk, status):
    task = get_object_or_404(Task, pk=pk)
    if not (request.user == task.assignee or request.user.is_superuser):
        return redirect('dashboard')

    status_choices = dict(Task.STATUS_CHOICES).keys()
    if status in status_choices:
        if (status == 'done' and not request.user.is_superuser) or \
           (status == 'new' and task.status != 'in_progress') or \
           (status == 'in_progress' and task.status not in ['new', 'in_qa']) or \
           (status == 'in_qa' and task.status not in ['in_progress', 'ready']) or \
           (status == 'ready' and task.status not in ['in_qa', 'done']):
            return redirect('dashboard')

        task.status = status
        task.save()

    return redirect('dashboard')


class TaskByStatusView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        status = self.kwargs['status']
        return Task.objects.filter(status=status).order_by('-updated_at')
