from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    # message = "You do not have the permission to perform this action"
    
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superadmin:
            return True
        return False
