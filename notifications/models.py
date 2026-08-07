from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User


class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
=======
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200, blank=True, default='')
    message = models.TextField()
    link = models.URLField(max_length=500, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
>>>>>>> samir

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
<<<<<<< HEAD
        return self.title
=======
        return f"{self.user.username} - {self.title or self.message[:30]}"
>>>>>>> samir
