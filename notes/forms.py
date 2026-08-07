from django import forms
from .models import Note

<<<<<<< HEAD

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write a note..."
                }
            )
=======
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']  # include both fields
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
>>>>>>> samir
        }