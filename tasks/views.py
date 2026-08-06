from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    tasks = Task.objects.all()
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'total': tasks.count()})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            
            # Send email notification to assigned user
            if task.assigned_to and task.assigned_to.email:
                send_mail(
                    subject=f'New Task Assigned: {task.title}',
                    message=f'''Hi {task.assigned_to.username},

You have been assigned a new task in My CRM.

Task: {task.title}
Due Date: {task.due_date}
Status: {task.get_status_display()}

Notes: {task.notes or 'No notes'}

Please complete it on time.
- My CRM System''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[task.assigned_to.email],
                    fail_silently=True,
                )
            
            messages.success(request, 'Task created and email sent successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})