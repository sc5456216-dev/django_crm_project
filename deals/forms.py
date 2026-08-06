from django import forms
from .models import Deal

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['title', 'value', 'stage', 'contact', 'company', 'assigned_to', 'expected_close_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'stage': forms.Select(attrs={'class': 'form-select'}),
            'contact': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'expected_close_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }