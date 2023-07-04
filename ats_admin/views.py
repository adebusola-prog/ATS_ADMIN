from rest_framework import generics,  status, permissions, exceptions
from rest_framework.status import HTTP_403_FORBIDDEN
from accounts.models import CustomUser
from .serializers import CustomUserSuperAdminSerializer, CustomUserPictureUpdateSerializer, \
    CustomUserSubAdminSerializer
from .permissions import IsSuperAdmin
from .paginations import CustomPagination


class SuperAdminDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSuperAdminSerializer
    permission_classes = [IsSuperAdmin]

    def get_object(self):
        # Retrieve the super admin user
        return self.request.user

    # def get(self, request, *args, **kwargs):
    #     self.check_permissions(request)
    #     if not request.user.is_superadmin:
    #         raise exceptions.PermissionDenied(detail="You do not have permission to access this resource.",
    #                                            status=status.HTTP_403_FORBIDDEN)
    #     return self.retrieve(request, *args, **kwargs)


# this should be done by only the useradmin
class ProfilePictureUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserPictureUpdateSerializer
    permission_classes = [IsSuperAdmin]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.get_object()
        return context
    

class SubAdminCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSuperAdmin]

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     if not user.is_superadmin:
    #         raise exceptions.PermissionDenied(detail="You do not have permission to access this resource.",
    #                                            status=status.HTTP_403_FORBIDDEN)
    #     serializer.save()

    
class SubAdminListView(generics.ListAPIView):
    pagination_class = CustomPagination
    queryset = CustomUser.active_objects.filter(is_admin=True)
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSuperAdmin]