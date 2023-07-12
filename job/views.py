import csv
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import JobSerializer, JobApplicationListCreateSerializer, JobViewsSerializer,\
    RecentJobsSerializer, InterviewInvitationSerializer, LocationSerializer
from rest_framework.views import APIView
from django.utils import timezone, timesince
from datetime import datetime, timedelta
from .models import Job, JobViews, JobApplication, InterviewInvitation, Location
from ats_admin.permissions import IsAdmin, IsApplicantAccess
from ats_admin.paginations import JobPagination
from rest_framework.response import Response
from .mixins import CustomMessageCreateMixin, CustomMessageUpdateMixin, CustomMessageDestroyMixin
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_400_BAD_REQUEST
from dashboard.activity import ActivityLogJobMixin
from django.db.models import Count, F
from django.http import HttpResponse
from django.core.mail import send_mail



class LocationListAPIView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


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
        # instance.refresh_from_db(fields=['no_of_views'])
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save(posted_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_role = instance.role
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self._update_activity_log(serializer.instance, request, old_role)
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


class JobApplicantCreateAPIView(ActivityLogJobMixin, CustomMessageCreateMixin, CreateAPIView):
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsApplicantAccess]
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)


class JobApplicantListAPIView(ActivityLogJobMixin, ListAPIView):
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]


class JobApplicantDetailAPIView(ActivityLogJobMixin, RetrieveAPIView):
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
    

class DaysRecentJobsAPIView(APIView):
    serializer_class = RecentJobsSerializer
    permission_classes = [IsAdmin]

   
    def post(self, request, *args, **kwargs):
        today = timezone.now().date()
        days = self.request.data.get('days', None)
        print(days)
        if not days:
            days_ago = today - timedelta(days=7)
            recent_jobs = Job.active_objects.filter(created_at__gte=days_ago)
            serializer = self.serializer_class(recent_jobs, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        try:
            days = int(days)
        except ValueError:
            return Response({'error': 'Invalid number of days.'}, status=HTTP_400_BAD_REQUEST)

        days_ago = today - timedelta(days=days)
        recent_jobs = Job.active_objects.filter(created_at__gte=days_ago)
        serializer = self.serializer_class(recent_jobs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class ExportApplicantsCSVView(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, *args, **kwargs):
        selected_ids = request.data.get('selected_ids', "Pls select")
        approved_applicants = JobApplication.objects.filter(id__in=selected_ids).all()
        

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="approved_applicants.csv"'

        writer = csv.writer(response)
        writer.writerow(['first_name', 'last_name', 'email', 'phone_number'])

        for applicant in approved_applicants:
            if applicant.applicant:
                writer.writerow([
                    applicant.applicant.first_name if applicant.applicant.first_name else '',
                    applicant.applicant.last_name if applicant.applicant.last_name else '',
                    applicant.applicant.email if applicant.applicant.email else '',
                    applicant.applicant.phone_number if applicant.applicant.phone_number else '',
                ])

        return response
    

class ShortlistCandidateView(UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_shortlisted == False:
            instance.is_shortlisted = True
            instance.save()
            response = {
                "message": " Candidate shortlisted successfully"
            }
            return Response(response, status=HTTP_200_OK)
        else:
            response = {
                "message": "This candidate has been shortlisted before"
            }
            return Response(response, status=HTTP_400_BAD_REQUEST)
    

class InterviewInvitationAPIView(UpdateAPIView):
    queryset = JobApplication.shortlisted_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_invited_for_interview = True
        instance.save()
        serializer = InterviewInvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation = InterviewInvitation.objects.create(
            job_application=instance,
            title=serializer.validated_data.get('title'),
            content=serializer.validated_data.get('content'),
        )

        send_mail(
            invitation.title,
            invitation.content,
            "adebusolayeye@gmail.com",
            [instance.applicant.email],
            fail_silently=False,
        )
        response = {
            "message": "Interview invitations sent successfully."
        }
        return Response(response, status=HTTP_200_OK)
    


class HireCandidateView(UpdateAPIView):
    queryset = JobApplication.shortlisted_interview_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_hired == False and instance.is_rejected == False:
            instance.is_hired = True
            instance.save()
            response = {
                "message": " Candidate hired successfully"
            }
            return Response(response, status=HTTP_200_OK)
        
        elif instance.is_hired == True and instance.is_rejected == False:
            response = {
                "message": "This candidate has been hired previously"
            }
            return Response(response, status=HTTP_400_BAD_REQUEST)
        
        elif instance.is_hired == False and instance.is_rejected == True:
            instance.is_rejected == False
            instance.is_hired == True

            response = {
                "message": "This candidate previously rejected, has now been hired"
            }
            return Response(response, status=HTTP_200_OK)
        
class RejectCandidateView(UpdateAPIView):
    queryset = JobApplication.shortlisted_interview_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_hired == False and instance.is_rejected == False:
            instance.is_rejected = True
            instance.save()
            response = {
                "message": " Candidate rejected successfully"
            }
            return Response(response, status=HTTP_200_OK)
        
        elif instance.is_hired == False and instance.is_rejected == True:
            response = {
                "message": "This candidate has previously been rejected"
            }
            return Response(response, status=HTTP_400_BAD_REQUEST)
            
        
        elif instance.is_hired == True and instance.is_rejected == False:
            instance.is_hired == False
            instance.is_rejected == True
            response = {
            "message": "This candidate previously hired has now been rejected!!"
            }
            return Response(response, status=HTTP_200_OK)


class ApplicantJobListAPIView(ListAPIView):
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer


class ApplicantJobDetailAPIView(RetrieveAPIView):
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.no_of_views += 1
        # instance.refresh_from_db(fields=['no_of_views'])
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=HTTP_200_OK)