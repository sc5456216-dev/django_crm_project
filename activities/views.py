from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from .models import ActivityLog


@login_required
def activity_list(request):
    """
    Display a list of all activities with role-based filtering.
    
    - Admin: sees all activities
    - Sales Manager: sees all activities
    - Regular users: see only their own activities
    """
    
    # Get filter parameters from request
    action_filter = request.GET.get('action', '')
    user_filter = request.GET.get('user', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Base queryset based on user role
    if request.user.groups.filter(name='Admin').exists():
        activities = ActivityLog.objects.select_related('user').order_by('-created_at')
        
    elif request.user.groups.filter(name='Sales Manager').exists():
        activities = ActivityLog.objects.select_related('user').order_by('-created_at')
        
    else:
        # Regular users see only their own activities
        activities = ActivityLog.objects.filter(
            user=request.user
        ).select_related('user').order_by('-created_at')
    
    # Apply filters
    if action_filter:
        activities = activities.filter(action__icontains=action_filter)
    
    if user_filter:
        activities = activities.filter(user__username__icontains=user_filter)
    
    if date_from:
        try:
            date_from_parsed = timezone.datetime.strptime(date_from, '%Y-%m-%d')
            activities = activities.filter(created_at__date__gte=date_from_parsed.date())
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_parsed = timezone.datetime.strptime(date_to, '%Y-%m-%d')
            activities = activities.filter(created_at__date__lte=date_to_parsed.date())
        except ValueError:
            pass
    
    # Pagination
    paginator = Paginator(activities, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get unique actions for filter dropdown
    unique_actions = ActivityLog.objects.values_list('action', flat=True).distinct()
    
    # Get unique users for filter dropdown (only for admin/manager)
    if request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists():
        unique_users = ActivityLog.objects.values_list('user__username', flat=True).distinct()
    else:
        unique_users = []
    
    context = {
        'activities': page_obj,
        'action_filter': action_filter,
        'user_filter': user_filter,
        'date_from': date_from,
        'date_to': date_to,
        'unique_actions': unique_actions,
        'unique_users': unique_users,
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_manager': request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists(),
    }
    
    return render(request, 'activities/activity_list.html', context)


@login_required
def activity_detail(request, pk):
    """Display detailed view of a single activity."""
    
    activity = get_object_or_404(ActivityLog, pk=pk)
    
    # Check permissions
    if not request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists():
        if activity.user != request.user:
            messages.error(request, "You don't have permission to view this activity.")
            return redirect('activity_list')
    
    return render(request, 'activities/activity_detail.html', {
        'activity': activity,
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_manager': request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists(),
    })


@login_required
def activity_delete(request, pk):
    """Delete an activity (admin only)."""
    
    if not request.user.groups.filter(name='Admin').exists():
        messages.error(request, "Only administrators can delete activities.")
        return redirect('activity_list')
    
    activity = get_object_or_404(ActivityLog, pk=pk)
    
    if request.method == 'POST':
        activity.delete()
        messages.success(request, "Activity deleted successfully.")
        return redirect('activity_list')
    
    return render(request, 'activities/activity_confirm_delete.html', {
        'activity': activity,
    })


@login_required
def activity_clear_all(request):
    """Clear all activities (admin only)."""
    
    if not request.user.groups.filter(name='Admin').exists():
        messages.error(request, "Only administrators can clear all activities.")
        return redirect('activity_list')
    
    if request.method == 'POST':
        ActivityLog.objects.all().delete()
        messages.success(request, "All activities cleared successfully.")
        return redirect('activity_list')
    
    return render(request, 'activities/activity_confirm_clear.html')


@login_required
def activity_user_activities(request, username):
    """View activities for a specific user (admin/manager only)."""
    
    if not request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists():
        messages.error(request, "You don't have permission to view other users' activities.")
        return redirect('activity_list')
    
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)
    
    activities = ActivityLog.objects.filter(user=user).order_by('-created_at')
    
    return render(request, 'activities/activity_user_list.html', {
        'activities': activities,
        'target_user': user,
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_manager': request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists(),
    })