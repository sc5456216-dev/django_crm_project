from .models import ActivityLog


def create_activity(
    user,
    module,
    action,
    object_name,
    description=""
):

    if user.is_authenticated:

        ActivityLog.objects.create(
            user=user,
            module=module,
            action=action,
            object_name=object_name,
            description=description,
        )