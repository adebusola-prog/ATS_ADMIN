from django.shortcuts import render
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from ats_admin.permissions import IsAdmin
from ats_admin.paginations import JobPagination
from rest_framework.generics import ListAPIView

# Create your views here.
class ActivityLogListAPIView(ListAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdmin]
    pagination_class = JobPagination