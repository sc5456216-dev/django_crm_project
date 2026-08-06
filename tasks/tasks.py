from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_task_email_async(task_title, assigned_email, assigned_username, due_date, notes):
    send_mail(
        subject=f'New Task Assigned: {task_title}',
        message=f'''Hi {assigned_username},

You have been assigned a new task.

Task: {task_title}
Due Date: {due_date}
Notes: {notes or 'No notes'}

- My CRM''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[assigned_email],
        fail_silently=True,
    )
    return f"Email sent to {assigned_email}"