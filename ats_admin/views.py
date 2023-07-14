from rest_framework import generics
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import CustomUser
from .serializers import (
    CustomUserSuperAdminSerializer,
    CustomUserPictureUpdateSerializer,
    CustomUserSubAdminSerializer,
)
from .permissions import IsSuperAdmin, IsSubAdmin
from .paginations import CustomPagination



class SuperAdminDetailView(generics.RetrieveAPIView):
    """A user with the superadmin status can only view this"""
    queryset = CustomUser.active_objects.all()
    serializer_class = CustomUserSuperAdminSerializer
    permission_classes = [IsSuperAdmin]

    def get_object(self):
        return self.request.user

  
class ProfilePictureUpdateView(generics.UpdateAPIView):
    """Allows a Super Admin to update profile picture"""
    queryset = CustomUser.active_objects.all()
    serializer_class = CustomUserPictureUpdateSerializer
    permission_classes = [IsSuperAdmin]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.get_object()
        return context
    

class SubAdminCreateView(generics.CreateAPIView):
    """Create view for subadmins"""
    queryset = CustomUser.objects.all()
    permission_classes = [IsSuperAdmin]
    serializer_class = CustomUserSubAdminSerializer
   

class SubAdminListView(generics.ListAPIView):
    """Lists the subadmins created"""
    queryset = CustomUser.objects.filter(is_admin=True)
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSuperAdmin]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']


class SubAdminDetailView(generics.RetrieveAPIView):
    """retreives each sub admin"""
    queryset = CustomUser.objects.filter(is_admin=True)
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSuperAdmin]
    
    
class SubAdminProfileView(generics.RetrieveAPIView):
    """This view allows each subadmin to view their profile"""
    queryset = CustomUser.active_objects.all()
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSubAdmin]

    def get_object(self):
        return self.request.user


class SubAdminDeleteAPIView(DestroyAPIView):
    """Allows a super admin delete a subadmin"""
    serializer_class = CustomUserSubAdminSerializer
    queryset = CustomUser.active_objects.all()
    permission_classes = [IsSuperAdmin]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        response = {
            "message": "SubAdmin deleted successfully"
        }
        return Response(response, status=HTTP_200_OK)
    

