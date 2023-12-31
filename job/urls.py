from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import JobListCreateAPIView, JobDetailUpdateAPIView,\
    JobApplicantCreateAPIView, JobDeleteAPIView, JobApplicantDetailAPIView,\
    JobApplicantListAPIView, JobViewsListCreateAPIView, DaysRecentJobsAPIView, ExportApplicantsCSVView,\
    ShortlistCandidateView, ApplicantJobDetailAPIView, ApplicantJobListAPIView, LocationListAPIView,\
    InterviewInvitationAPIView, HireCandidateView, RejectCandidateView, JobApplicationFilterAPIView,\
    BulkShortlistCandidateView, BulkInterviewInvitationAPIView, BulkHireCandidateView, \
      BulkRejectCandidateView
from dashboard.views import ActivityLogListAdminAPIView, ActivityLogListNotificationAPIView


app_name = "jobs"

urlpatterns = [
    path('job_list_create', JobListCreateAPIView.as_view(), name='job_list_create'), 
    path('<int:pk>/job_detail_update', JobDetailUpdateAPIView.as_view(), name='job_detail_update'),
    path('<int:pk>/job_delete', JobDeleteAPIView.as_view(), name='job_delete'),

    path('job_application_create', JobApplicantCreateAPIView.as_view(), name='job_application_create'),
    path('job_application_list', JobApplicantListAPIView.as_view(), name='job_application_list'),
    path('<int:pk>/job_application_detail', JobApplicantDetailAPIView.as_view(), \
         name='job_application_detail'),

    path('applicant_job_list', ApplicantJobListAPIView.as_view(), name='applicant_job_list'),
    path('<int:pk>/applicant_job_detail', ApplicantJobDetailAPIView.as_view(), \
         name='applicant_job_detail'),
    path('job_views', JobViewsListCreateAPIView.as_view(), name='job_views'),
    path('activity_log', ActivityLogListAdminAPIView.as_view(), name='activity_log'),
    path('job_notification', ActivityLogListNotificationAPIView.as_view(), 
         name='job_notification'),

    path('days_ago_jobs', DaysRecentJobsAPIView.as_view(), name='five_days_ago'),
    path('export_csv', ExportApplicantsCSVView.as_view(), name='export_applicant'),
    
    path('job_application/<int:pk>/shortlist_candidate', ShortlistCandidateView.as_view(),\
          name='shortlist_candidate'),
    path('job_application/<int:pk>/interview_applicant', InterviewInvitationAPIView.as_view(),\
          name="interview_applicant"),
    path('job_application/<int:pk>/hire_candidate', HireCandidateView.as_view(),\
          name="hire_candidate"),
    path('job_application/<int:pk>/reject_candidate', RejectCandidateView.as_view(),\
          name="reject_candidate"),
    
    path('location_list', LocationListAPIView.as_view(), name="location_list"),
    path('application_filter', JobApplicationFilterAPIView.as_view(), name='application_filter'),

    path('bulk_shortlist', BulkShortlistCandidateView.as_view(), name='bulk_shortlist'),
    path('bulk_invite', BulkInterviewInvitationAPIView.as_view(), name="bulk_invite"),
    path('bulk_hire', BulkHireCandidateView.as_view(), name="bulk_hire"),
    path('bulk_reject', BulkRejectCandidateView.as_view(), name='bulk_reject')
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

