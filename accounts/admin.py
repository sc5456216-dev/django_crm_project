from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group


# Custom UserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups']
    list_filter = ['groups', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Role'


# Unregister default User
if admin.site.is_registered(User):
    admin.site.unregister(User)

# Register User with custom admin
admin.site.register(User, CustomUserAdmin)

# Register Groups (if not already registered)
if not admin.site.is_registered(Group):
    admin.site.register(Group, GroupAdmin)