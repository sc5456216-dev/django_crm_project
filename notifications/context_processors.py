from .models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        latest = request.user.notifications.all()[:5]
        return {
            'unread_count': unread_count,
            'latest_notifications': latest,
        }
    return {}