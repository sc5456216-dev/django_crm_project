from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from notes.models import Note
from tasks.models import Task
from .utils import create_notification

@receiver(post_save, sender=Note)
def note_created_notification(sender, instance, created, **kwargs):
    if created:
        users = User.objects.exclude(id=instance.author.id)
        for user in users:
            create_notification(
                user=user,
                title="New Note",
                message=f"New note: {instance.title or instance.content[:30]} by {instance.author.username}",
                link=f"/notes/{instance.pk}/update/"
            )

@receiver(post_save, sender=Task)
def task_assigned_notification(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        create_notification(
            user=instance.assigned_to,
            title="Task Assigned",
            message=f"New task: {instance.title}",
            link=f"/tasks/{instance.pk}/"
        )