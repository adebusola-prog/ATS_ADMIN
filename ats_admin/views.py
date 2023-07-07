from rest_framework import generics
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
        return self.request.user

  
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

    
class SubAdminListView(generics.ListAPIView):
    queryset = CustomUser.active_objects.filter(is_admin=True)
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSuperAdmin]
    pagination_class = CustomPagination


class SubAdminDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.active_objects.filter(is_admin=True)
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSuperAdmin]
    

