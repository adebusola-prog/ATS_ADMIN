from rest_framework import generics
from rest_framework.generics import DestroyAPIView
from rest_framework.status import HTTP_403_FORBIDDEN
from accounts.models import CustomUser
from .serializers import CustomUserSuperAdminSerializer, CustomUserPictureUpdateSerializer, \
    CustomUserSubAdminSerializer
from .permissions import IsSuperAdmin, IsSubAdmin
from .paginations import CustomPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django_filters import rest_framework 



class SuperAdminDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.active_objects.all()
    serializer_class = CustomUserSuperAdminSerializer
    permission_classes = [IsSuperAdmin]

    def get_object(self):
        return self.request.user

  
class ProfilePictureUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.active_objects.all()
    serializer_class = CustomUserPictureUpdateSerializer
    permission_classes = [IsSuperAdmin]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.get_object()
        return context
    


class SubAdminFilter(rest_framework.FilterSet):
    subadmin_name = rest_framework.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


class SubAdminCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsSuperAdmin]
    # serializer_class = CustomUserSubAdminSerializer
   
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_class = SubAdminFilter
    # search_fields = ['first_name', 'last_name']

    
class SubAdminListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_admin=True)
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSuperAdmin]
    pagination_class = CustomPagination


class SubAdminDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(is_admin=True)
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSuperAdmin]
    
    
class SubAdminProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.active_objects.all()
    serializer_class = CustomUserSubAdminSerializer
    permission_classes = [IsSubAdmin]

    def get_object(self):
        return self.request.user


class SubAdminDeleteAPIView(DestroyAPIView):
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