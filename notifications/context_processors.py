from .models import Notification

<<<<<<< HEAD

def notification_count(request):

    if request.user.is_authenticated:

        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    else:
        count = 0

    return {
        "notification_count": count
    }
=======
def notification_context(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        latest = request.user.notifications.all()[:5]
        return {
            'unread_count': unread_count,
            'latest_notifications': latest,
        }
    return {}
>>>>>>> samir
