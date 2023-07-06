from django.contrib import admin
from .models import CustomUser, PermissionLevel


admin.site.register(CustomUser)
admin.site.register(PermissionLevel)
