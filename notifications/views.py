from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Notification


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    )

    return render(
        request,
        "notifications/notification_list.html",
        {"notifications": notifications},
    )


@login_required
def mark_as_read(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect("notification_list")


@login_required
def delete_notification(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    notification.delete()

    return redirect("notification_list")
