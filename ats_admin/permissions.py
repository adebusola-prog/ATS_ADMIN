from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superadmin:
            return True
        raise PermissionDenied("You are not a superadmin!!. You are not allowed to perform this operation.")


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superadmin or request.user.is_admin :
            return True
        raise PermissionDenied("You are not an admin!!!. You are not allowed to perform this operation.")
    
class IsApplicantAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superadmin == False\
            or request.user.is_admin == False:
            return True
        raise PermissionDenied("You are not allowed to perform this operation.")