from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import ActivityLog


@login_required
def activity_list(request):

    if request.user.groups.filter(name='Admin').exists():
        activities = ActivityLog.objects.select_related("user").order_by("-created_at")

    elif request.user.groups.filter(name='Sales Manager').exists():
        activities = ActivityLog.objects.select_related("user").order_by("-created_at")

    else:
        activities = ActivityLog.objects.filter(
            user=request.user
        ).select_related("user").order_by("-created_at")

    return render(
        request,
        "activities/activity_list.html",
        {
            "activities": activities,
        },
    )