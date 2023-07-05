from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superadmin:
            return True
        raise PermissionDenied("You are not a superadmin!!. You are not allowed to perform this operation.")
