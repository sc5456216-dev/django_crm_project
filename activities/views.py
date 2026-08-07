from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ActivityLog

@login_required
def activity_list(request):
    activities = ActivityLog.objects.all().order_by('-created_at')
    return render(request, 'activities/activity_list.html', {'activities': activities})
