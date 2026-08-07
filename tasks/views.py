from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Task
from .forms import TaskForm
from .tasks import send_task_email_async

from accounts.decorators import admin_required, manager_required
from activities.utils import create_activity
from notifications.utils import create_notification


@login_required
def task_list(request):
    if request.user.groups.filter(name="Sales Rep").exists():
        tasks = Task.objects.filter(assigned_to=request.user)
    else:
        tasks = Task.objects.all()

    status = request.GET.get("status")

    if status:
        tasks = tasks.filter(status=status)

    context = {
        "tasks": tasks,
        "total": tasks.count(),
        "is_admin": request.user.groups.filter(name="Admin").exists(),
        "is_manager": request.user.groups.filter(
            name__in=["Admin", "Sales Manager"]
        ).exists(),
    }

    return render(request, "tasks/task_list.html", context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user.groups.filter(name="Sales Rep").exists():
        if task.assigned_to != request.user:
            raise PermissionDenied(
                "You can only view your assigned tasks."
            )

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
        },
    )


@login_required
@manager_required
def task_create(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save()

            # Activity Log
            create_activity(
                user=request.user,
                module="Task",
                action="CREATE",
                object_name=task.title,
                description=f"Created task '{task.title}'",
            )

            # Notification
            if task.assigned_to:
                create_notification(
                    user=task.assigned_to,
                    title="New Task Assigned",
                    message=f"You have been assigned a new task: '{task.title}'.",
                )

            # Email
            if task.assigned_to and task.assigned_to.email:
                send_task_email_async.delay(
                    task_title=task.title,
                    assigned_email=task.assigned_to.email,
                    assigned_username=task.assigned_to.username,
                    due_date=str(task.due_date),
                    notes=task.notes or "",
                )

            messages.success(
                request,
                "Task created successfully. Email and notification sent.",
            )

            return redirect("task_list")

    else:
        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
        },
    )


@login_required
@manager_required
def task_update(request, pk):

    task = get_object_or_404(Task, pk=pk)

    old_status = task.status
    old_assigned_to = task.assigned_to

    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)

        if form.is_valid():

            task = form.save()

            # Activity Log
            create_activity(
                user=request.user,
                module="Task",
                action="UPDATE",
                object_name=task.title,
                description=f"Updated task '{task.title}'",
            )

            # Status Change
            if old_status != task.status:

                create_activity(
                    user=request.user,
                    module="Task",
                    action="UPDATE",
                    object_name=task.title,
                    description=(
                        f"Changed task status "
                        f"from '{old_status}' "
                        f"to '{task.status}'"
                    ),
                )

                if task.assigned_to:
                    create_notification(
                        user=task.assigned_to,
                        title="Task Status Updated",
                        message=(
                            f"Task '{task.title}' "
                            f"is now '{task.status}'."
                        ),
                    )

            # Assignment Change
            if old_assigned_to != task.assigned_to and task.assigned_to:

                create_notification(
                    user=task.assigned_to,
                    title="Task Assigned",
                    message=f"You have been assigned '{task.title}'.",
                )

            messages.success(
                request,
                "Task updated successfully!",
            )

            return redirect("task_list")

    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
        },
    )


@login_required
@admin_required
def task_delete(request, pk):

    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":

        create_activity(
            user=request.user,
            module="Task",
            action="DELETE",
            object_name=task.title,
            description=f"Deleted task '{task.title}'",
        )

        if task.assigned_to:

            create_notification(
                user=task.assigned_to,
                title="Task Deleted",
                message=f"The task '{task.title}' has been deleted.",
            )

        task.delete()

        messages.success(
            request,
            "Task deleted successfully!",
        )

        return redirect("task_list")

    return render(
        request,
        "tasks/task_confirm_delete.html",
        {
            "task": task,
        },
    )