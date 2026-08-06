from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        rep_group, _ = Group.objects.get_or_create(name='Sales Rep')
        instance.groups.add(rep_group)