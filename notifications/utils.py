from .models import Notification

<<<<<<< HEAD

def create_notification(user, title, message):
=======
def create_notification(user, title, message, link=None):
>>>>>>> samir
    """
    Create a notification only if an identical unread notification
    doesn't already exist.
    """
<<<<<<< HEAD

=======
>>>>>>> samir
    notification, created = Notification.objects.get_or_create(
        user=user,
        title=title,
        message=message,
        is_read=False,
<<<<<<< HEAD
    )

=======
        defaults={'link': link}
    )
>>>>>>> samir
    return notification