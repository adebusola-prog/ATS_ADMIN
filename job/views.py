import csv
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import JobSerializer, JobApplicationListCreateSerializer, JobViewsSerializer,\
    RecentJobsSerializer, InterviewInvitationSerializer, LocationSerializer,\
          IDValidationCustomSerializer
from rest_framework.views import APIView
from django.utils import timezone, timesince
from datetime import datetime, timedelta
from .models import Job, JobViews, JobApplication, InterviewInvitation, Location
from ats_admin.permissions import IsAdmin, IsApplicantAccess
from ats_admin.paginations import JobPagination
from rest_framework import status
from rest_framework.response import Response
from .mixins import CustomMessageCreateMixin, CustomMessageUpdateMixin, CustomMessageDestroyMixin
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_400_BAD_REQUEST
from dashboard.activity import ActivityLogJobMixin
from django.db.models import Count, F
from django.http import HttpResponse
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
import rest_framework


class LocationListAPIView(ListAPIView):
    """Lists all the locations"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ApplicantJobListAPIView(ListAPIView):
    """A public view that lists all the jobs"""
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer


class ApplicantJobDetailAPIView(RetrieveAPIView):
    """A view to view each job's detail"""
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.no_of_views += 1
        # instance.refresh_from_db(fields=['no_of_views'])
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class JobListCreateAPIView(ActivityLogJobMixin, CustomMessageCreateMixin, ListCreateAPIView):
    """A view that Lists a job and
       Create a job
    """
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    pagination_class = JobPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['role', 'skill_level', 'job_type', 'job_schedule', 'location__name']
    search_fields = ['role', 'skill_level', 'job_type', 'job_schedule', 'location__name']

    
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
        return Response(response, status=status.HTTP_200_OK)


class JobDetailUpdateAPIView(ActivityLogJobMixin, CustomMessageUpdateMixin, RetrieveUpdateAPIView):
    """Retreives and Updates a job depending on the method used"""
    queryset = Job.active_objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.no_of_views += 1
        # instance.refresh_from_db(fields=['no_of_views'])
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
        return Response(response, status=status.HTTP_200_OK)


class JobDeleteAPIView(CustomMessageDestroyMixin, ActivityLogJobMixin, DestroyAPIView):
    """To delete a job"""
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    queryset = Job.active_objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        old_role = instance.role
        instance.is_active = False
        instance.save()
        self._delete_activity_log(instance, request, old_role)
        response = {
            "message": "Job deleted successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


class JobApplicantCreateAPIView(ActivityLogJobMixin, CustomMessageCreateMixin, CreateAPIView):
    """Allows a user to apply for a job"""
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsApplicantAccess]
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self._create_application_activity_log(serializer.instance, request)
        response = {
            "message": "New Application created successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


class JobApplicantListAPIView(ActivityLogJobMixin, ListAPIView):
    """Lists all the job application"""
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]


class JobApplicantDetailAPIView(ActivityLogJobMixin, RetrieveAPIView):
    """Retreives the full detais of each applicants"""
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]   


class JobViewsListCreateAPIView(ListCreateAPIView):
    """No of times the job was viewed"""
    queryset = JobViews.objects.all()
    serializer_class = JobViewsSerializer

    def get(self, request, *args, **kwargs):
        job_id = request.query_params.get('job_id')
        job_views = JobViews.active_objects.filter(job_id=job_id).\
            annotate(num_views=Count('viewer_ip'))
        serializer = self.get_serializer(job_views, many=True)
        return Response(serializer.data)
    

class DaysRecentJobsAPIView(APIView):
    """Return jobs according to number of days"""
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            days = int(days)
        except ValueError:
            return Response({'error': 'Invalid number of days.'}, status=HTTP_400_BAD_REQUEST)

        days_ago = today - timedelta(days=days)
        recent_jobs = Job.active_objects.filter(created_at__gte=days_ago)
        serializer = self.serializer_class(recent_jobs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class ExportApplicantsCSVView(APIView):
    """Exports all selected applicants to a csv file"""
    permission_classes = [IsAdmin]
    serializer_class = IDValidationCustomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected_ids = serializer.validated_data['selected_ids']
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
    """
    API view for shortlisting a selected applicant.
    Allows marking an applicant as shortlisted for further consideration.
    """
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
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "This candidate has been shortlisted before"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    

class InterviewInvitationAPIView(UpdateAPIView):
    """Invites shortlisted applicant for interview"""
    queryset = JobApplication.shortlisted_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_invited_for_interview == False:
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
            return Response(response, status=status.HTTP_200_OK)
        return Response({"message":"This User has been sent an interview request"})



class HireCandidateView(UpdateAPIView):
    """Use for hiring applicants"""
    queryset = JobApplication.interview_objects.all()
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
            instance.is_rejected = False
            instance.is_hired = True
            instance.save()
            response = {
                "message": "This candidate previously rejected, has now been hired"
            }
            return Response(response, status=status.HTTP_200_OK)
        

class RejectCandidateView(UpdateAPIView):
    """Performs candidate rejection"""
    queryset = JobApplication.interview_objects.all()
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
            return Response(response, status=status.HTTP_200_OK)
        
        elif instance.is_hired == False and instance.is_rejected == True:
            response = {
                "message": "This candidate has previously been rejected"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
        elif instance.is_hired == True and instance.is_rejected == False:
            instance.is_hired = False
            instance.is_rejected = True
            instance.save()
            response = {
            "message": "This candidate previously hired has now been rejected!!"
            }
            return Response(response, status=status.HTTP_200_OK)



class JobApplicationFilterAPIView(ListAPIView):
    """
    API view for filtering job applications by their status.
    Query parameter 'status' can be used to filter by different statuses.
    """
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        queryset = super().get_queryset()

        if status == 'shortlisted':
            queryset = JobApplication.shortlisted_only_objects.filter()
            print(queryset)
        elif status == 'interviewed':
            queryset = JobApplication.interview_only_objects.filter()
            print(queryset)
        elif status == 'hired':
            queryset = JobApplication.hired_objects.filter()
            print(queryset)
        elif status == 'rejected':
            queryset = JobApplication.rejected_objects.filter()
            print(queryset)

        return queryset


class BulkShortlistCandidateView(UpdateAPIView):
    """
    API view for bulk shortlisting candidates.
    Allows shortlisting multiple job applications at once.
    Only accessible by admin users.
    """
    queryset = JobApplication.active_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        serializer = IDValidationCustomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected_ids = serializer.validated_data.get('selected_ids') 
        applicants = JobApplication.active_objects.filter(id__in=selected_ids, is_shortlisted=False)
        
        if applicants.exists():
            applicants.update(is_shortlisted=True)
            response = {
                "message": "Candidates shortlisted successfully"
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "No candidates to update"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        

class BulkInterviewInvitationAPIView(UpdateAPIView):
    """
    API view for bulk sending interview invitations.
    Allows sending interview invitations to multiple shortlisted job applications at once.
    Only accessible by admin users.
    """
    queryset = JobApplication.shortlisted_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        serializer = IDValidationCustomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected_ids = serializer.validated_data.get('selected_ids') 
        applicants = JobApplication.shortlisted_objects.filter(id__in=selected_ids, \
                                is_invited_for_interview=False)
        applicants.update(is_invited_for_interview=True)

        serializer = InterviewInvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for applicant in applicants:
            if not applicant.is_interviewed:
                invitation = InterviewInvitation.objects.create(
                    job_application=applicant,
                    title=serializer.validated_data.get('title'),
                    content=serializer.validated_data.get('content'),
                )

                send_mail(
                    invitation.title,
                    invitation.content,
                    "adebusolayeye@gmail.com",
                    [applicant.applicant.email],
                    fail_silently=False,
                )

        response = {
            "message": "Interview invitations sent successfully."
        }
        return Response(response, status=HTTP_200_OK)



class BulkHireCandidateView(UpdateAPIView):
    """
    API view for bulk hiring candidates.
    Allows hiring multiple candidates from the shortlisted applicants who have been interviewed.
    Only accessible by admin users.
    """
    queryset = JobApplication.interview_only_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        serializer = IDValidationCustomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected_ids = serializer.validated_data.get('selected_ids') 
        applicants = JobApplication.interview_only_objects.filter(id__in=selected_ids)
        rejected_once = JobApplication.rejected_objects.filter(id__in=selected_ids)
       
        applicants.update(is_hired=True)
        response = {
            "message": " Candidate hired successfully"
        }
        if rejected_once:
            rejected_once.update(is_rejected=False, is_hired=True)
            response = {
                "message": "Candidate once rejected has now been hired"
        }
        return Response(response, status=HTTP_200_OK)
            
class BulkRejectCandidateView(UpdateAPIView):
    """
    API view for bulk rejecting candidates.
    Allows rejecting multiple candidates from the shortlisted applicants who have been interviewed.
    Only accessible by admin users.
    """
    queryset = JobApplication.interview_only_objects.all()
    serializer_class = JobApplicationListCreateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        serializer = IDValidationCustomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected_ids = serializer.validated_data.get('selected_ids') 
        applicants = JobApplication.interview_only_objects.filter(id__in=selected_ids)
        hired_once = JobApplication.hired_objects.filter(id__in=selected_ids)
       
        applicants.update(is_rejected=True)
        response = {
            "message": "Candidates rejected successfully"
        }

        if hired_once.exists():
            hired_once.update(is_hired=False, is_rejected=True)
            response["message"] = "Candidates previously hired have now been rejected"
        
        return Response(response, status=HTTP_200_OK)  