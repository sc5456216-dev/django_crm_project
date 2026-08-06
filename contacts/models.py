from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('customer', 'Customer'),
        ('partner', 'Partner'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



class ContactAttachment(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='contact_attachments/%Y/%m/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.contact} - {self.file.name}"