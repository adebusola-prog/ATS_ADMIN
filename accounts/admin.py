from django.contrib import admin
from .models import CustomUser, PermissionLevel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class UserAdmin(BaseUserAdmin):
    ordering = ('email',)  # Set the ordering field to 'email'
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',
             'is_admin',  'is_superadmin', 'last_login', 'date_joined')  # Add 'role', 'is_staff', and 'is_active' to the list_display field
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'position')  # Add 'role' to the list_filter field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', "is_admin", "is_superadmin",
                     'position', 'permission_level', 'date_of_birth', 'profile_picture')}),
        # ("Dates", {"fields": ("last_login",)})

    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'username'),
        }),
    )

admin.site.register(CustomUser, UserAdmin)
admin.site.register(PermissionLevel)