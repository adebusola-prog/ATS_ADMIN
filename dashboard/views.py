from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import ListAPIView

from job.models import Job, JobApplication
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from ats_admin.permissions import IsAdmin
from ats_admin.paginations import JobPagination, NotificationPagination


class ActivityLogListAdminAPIView(ListAPIView):
    """
    API view that lists the activity logs of subadmins on Jobs.
    """
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdmin]
    pagination_class = JobPagination

    def get_queryset(self):
        """
        Retrieve the queryset of activity logs filtered by content type.
        """
        content_type = ContentType.objects.get_for_model(Job)
        print(content_type)
        queryset = ActivityLog.objects.filter(content_type=content_type)
        return queryset


class ActivityLogListNotificationAPIView(ListAPIView):
    """Logs the activities of applicants"""
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdmin]
    pagination_class = NotificationPagination

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(JobApplication)
        queryset = ActivityLog.objects.filter(content_type=content_type)
        return queryset


