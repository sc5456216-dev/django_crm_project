from .models import Notification


def create_notification(user, title, message):
    """
    Create a notification only if an identical unread notification
    doesn't already exist.
    """

    notification, created = Notification.objects.get_or_create(
        user=user,
        title=title,
        message=message,
        is_read=False,
    )

    return notification