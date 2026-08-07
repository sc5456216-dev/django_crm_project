from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "module",
        "action",
        "object_name",
        "created_at",
    )

    list_filter = (
        "module",
        "action",
        "created_at",
    )

    search_fields = (
        "user__username",
        "object_name",
    )