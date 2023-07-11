from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import JobListCreateAPIView, JobDetailUpdateAPIView,\
    JobApplicantCreateAPIView, JobDeleteAPIView, JobApplicantDetailAPIView,\
    JobApplicantListAPIView, JobViewsListCreateAPIView, DaysRecentJobsAPIView, ExportApplicantsCSVView,\
    ShortlistCandidateView, ApplicantJobDetailAPIView, ApplicantJobListAPIView
from dashboard.views import ActivityLogListAPIView


app_name = "jobs"

urlpatterns = [
    path('job_list_create', JobListCreateAPIView.as_view(), name='job_list_create'), 
    path('<int:pk>/job_detail_update', JobDetailUpdateAPIView.as_view(), name='job_detail_update'),
    path('<int:pk>/job_delete', JobDeleteAPIView.as_view(), name='job_delete'),

    path('job_application_create', JobApplicantCreateAPIView.as_view(), name='job_application_create'),
    path('job_application_list', JobApplicantListAPIView.as_view(), name='job_application_list'),
    path('<int:pk>/job_application_detail', JobApplicantDetailAPIView.as_view(), name='job_application_detail'),

    path('applicant_job_list', ApplicantJobListAPIView.as_view(), name='applicant_job_list'),
    path('<int:pk>/applicant_job_detail', ApplicantJobDetailAPIView.as_view(), name='applicant_job_detail'),
    path('job_views', JobViewsListCreateAPIView.as_view(), name='job_views'),
    path('activity_log', ActivityLogListAPIView.as_view(), name='activity_log'),

    path('days_ago_jobs', DaysRecentJobsAPIView.as_view(), name='five_days_ago'),
    path('export_csv', ExportApplicantsCSVView.as_view(), name='export_applicant'),
    path('job_application/<int:pk>/shortlist_candidate', ShortlistCandidateView.as_view(), name='shortlist_candidate')
   
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

