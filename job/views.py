from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    CreateAPIView, ListAPIView, RetrieveAPIView
from .serializers import JobSerializer, JobApplicationListCreateSerializer
from .models import Job, JobApplication
from ats_admin.permissions import IsAdmin, IsApplicantAccess
from ats_admin.paginations import JobPagination
from rest_framework.response import Response
from .mixins import CustomMessageCreateMixin, CustomMessageUpdateMixin
from rest_framework.status import HTTP_204_NO_CONTENT


class JobListCreateAPIView(CustomMessageCreateMixin, ListCreateAPIView):
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    pagination_class = JobPagination
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class JobDetailUpdateAPIView(CustomMessageUpdateMixin, RetrieveUpdateAPIView):
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    
    def perform_update(self, serializer):
        serializer.save(posted_by=self.request.user)


class JobDeleteAPIView(DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=HTTP_204_NO_CONTENT)
    
class JobApplicantCreateAPIView(CustomMessageCreateMixin, CreateAPIView):
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsApplicantAccess]
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)


class JobApplicantListAPIView(ListAPIView):
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]


class JobApplicantDetailAPIView(RetrieveAPIView):
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]   


