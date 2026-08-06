from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task


class Command(BaseCommand):
    help = 'Send email reminders for tasks due tomorrow'

    def handle(self, *args, **kwargs):
        tomorrow = timezone.now() + timedelta(days=1)
        tasks = Task.objects.filter(
            status__in=['pending', 'in_progress'],
            due_date__date=tomorrow.date()
        )
        
        sent = 0
        for task in tasks:
            if task.assigned_to and task.assigned_to.email:
                send_mail(
                    subject=f'Reminder: Task Due Tomorrow - {task.title}',
                    message=f'''Hi {task.assigned_to.username},

This is a reminder that your task "{task.title}" is due tomorrow ({task.due_date.strftime('%Y-%m-%d %H:%M')}).

Please complete it on time.
- My CRM System''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[task.assigned_to.email],
                    fail_silently=True,
                )
                sent += 1
        
        self.stdout.write(self.style.SUCCESS(f'Sent {sent} reminder emails'))