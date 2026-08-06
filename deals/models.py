from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact
from companies.models import Company

class Deal(models.Model):
    STAGE_CHOICES = [
        ('lead', 'Lead'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]
    
    title = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='lead')
    
    contact = models.ForeignKey(
        Contact, 
        on_delete=models.CASCADE, 
        related_name='deals'
    )
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='deals'
    )
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deals'
    )
    
    expected_close_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - Rs. {self.value}"