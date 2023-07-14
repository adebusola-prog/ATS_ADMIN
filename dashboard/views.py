from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from ats_admin.permissions import IsAdmin
from ats_admin.paginations import JobPagination
from rest_framework.generics import ListAPIView
from job.models import Job, JobApplication


# Create your views here.
class ActivityLogListAdminAPIView(ListAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdmin]
    pagination_class = JobPagination

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(Job)
        queryset = ActivityLog.objects.filter(content_type__in=content_type.values())
        return queryset


class ActivityLogListNotificationAPIView(ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdmin]
    pagination_class = JobPagination

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(JobApplication)
        queryset = ActivityLog.objects.filter(content_type__in=content_type.values())
        return queryset


