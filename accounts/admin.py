from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, PermissionLevel


class UserAdmin(BaseUserAdmin):
    ordering = ('email',) 
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',
             'is_admin',  'is_superadmin', 'last_login', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'position')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', "is_admin", "is_superadmin",
                   "phone_number", 'position', 'permission_level', 'date_of_birth', 'profile_picture')}),
        # ("Dates", {"fields": ("last_login",)})

    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name',
             'last_name', 'username', 'date_of_birth'),
        }),
    )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(PermissionLevel)