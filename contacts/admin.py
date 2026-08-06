from django.contrib import admin
from .models import Contact, ContactAttachment

class AttachmentInline(admin.TabularInline):
    model = ContactAttachment
    extra = 1

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]

@admin.register(ContactAttachment)
class ContactAttachmentAdmin(admin.ModelAdmin):
    list_display = ['contact', 'description', 'uploaded_at']