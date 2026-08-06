from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Task
from .forms import TaskForm
from accounts.decorators import admin_required, manager_required
from .tasks import send_task_email_async


@login_required
def task_list(request):
    if request.user.groups.filter(name='Sales Rep').exists():
        tasks = Task.objects.filter(assigned_to=request.user)
    else:
        tasks = Task.objects.all()

    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'total': tasks.count(),
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_manager': request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists(),
    })


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user.groups.filter(name='Sales Rep').exists():
        if task.assigned_to != request.user:
            raise PermissionDenied("You can only view your assigned tasks.")

    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
@manager_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()

            # Send email ASYNCHRONOUSLY via Celery
            if task.assigned_to and task.assigned_to.email:
                send_task_email_async.delay(
                    task_title=task.title,
                    assigned_email=task.assigned_to.email,
                    assigned_username=task.assigned_to.username,
                    due_date=str(task.due_date),
                    notes=task.notes or ''
                )

            messages.success(request, 'Task created! Email will be sent shortly.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
@manager_required
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
@admin_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})