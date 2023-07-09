from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    CreateAPIView, ListAPIView, RetrieveAPIView
from .serializers import JobSerializer, JobApplicationListCreateSerializer, JobViewsSerializer
from .models import Job, JobViews, JobApplication
from ats_admin.permissions import IsAdmin, IsApplicantAccess
from ats_admin.paginations import JobPagination
from rest_framework.response import Response
from .mixins import CustomMessageCreateMixin, CustomMessageUpdateMixin, CustomMessageDestroyMixin
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from dashboard.activity import ActivityLogMixin, ActivityLogJobMixin
from django.db.models import Count, F


class JobListCreateAPIView(ActivityLogJobMixin, CustomMessageCreateMixin, ListCreateAPIView):
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    pagination_class = JobPagination
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self._create_activity_log(serializer.instance, request)
        response = {
            "message": "New Job created successfully"
        }
        return Response(response, status=HTTP_200_OK)


class JobDetailUpdateAPIView(ActivityLogJobMixin, CustomMessageUpdateMixin, RetrieveUpdateAPIView):
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.no_of_views += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save(posted_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        instance.no_of_views = F('no_of_views')+1
        print(instance.no_of_views)
        instance.refresh_from_db(fields=['no_of_views'])
        instance.save()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self._update_activity_log(serializer.instance, request)
        response = {
            "message": "Job updated successfully"
        }
        return Response(response, status=HTTP_200_OK)


class JobDeleteAPIView(CustomMessageDestroyMixin, ActivityLogJobMixin, DestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    queryset = Job.active_objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        self._delete_activity_log(instance, request)
        response = {
            "message": "Job deleted successfully"
        }
        return Response(response, status=HTTP_200_OK)


class JobApplicantCreateAPIView(ActivityLogMixin, CustomMessageCreateMixin, CreateAPIView):
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsApplicantAccess]
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)


class JobApplicantListAPIView(ActivityLogMixin, ListAPIView):
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]


class JobApplicantDetailAPIView(ActivityLogMixin, RetrieveAPIView):
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]   


class JobViewsListCreateAPIView(ListCreateAPIView):
    queryset = JobViews.objects.all()
    serializer_class = JobViewsSerializer

    def get(self, request, *args, **kwargs):
        job_id = request.query_params.get('job_id')
        job_views = JobViews.active_objects.filter(job_id=job_id).annotate(num_views=Count('viewer_ip'))
        serializer = self.get_serializer(job_views, many=True)
        return Response(serializer.data)
