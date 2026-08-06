from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact
from deals.models import Deal

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return self.title