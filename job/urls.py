from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import JobListCreateAPIView, JobDetailUpdateAPIView,\
    JobApplicantCreateAPIView, JobDeleteAPIView, JobApplicantDetailAPIView,\
    JobApplicantListAPIView, JobViewsListCreateAPIView, SevenDaysRecentJobsAPIView, \
    FiveDaysRecentJobsAPIView, ThreeDaysRecentJobsAPIView, OneDayRecentJobsAPIView
from dashboard.views import ActivityLogListAPIView



app_name = "jobs"

urlpatterns = [
    path('job_list_create', JobListCreateAPIView.as_view(), name='job_list_create'), 
    path('<int:pk>/job_detail_update', JobDetailUpdateAPIView.as_view(), name='job_detail_update'),
    path('<int:pk>/job_delete', JobDeleteAPIView.as_view(), name='job_delete'),

    path('job_application_create', JobApplicantCreateAPIView.as_view(), name='job_application_create'),
    path('job_application_list', JobApplicantListAPIView.as_view(), name='job_application_list'),
    path('<int:pk>/job_application_detail', JobApplicantDetailAPIView.as_view(), name='job_application_detail'),

    path('job_views', JobViewsListCreateAPIView.as_view(), name='job_views'),
    path('activity_log', ActivityLogListAPIView.as_view(), name='activity_log'),
    path('seven_days_ago', SevenDaysRecentJobsAPIView.as_view(), name='seven_days_ago'),
    path('five_days_ago', FiveDaysRecentJobsAPIView.as_view(), name='five_days_ago'),
    path('three_days_ago', ThreeDaysRecentJobsAPIView.as_view(), name='three_days_ago'),
    path('one_day_ago', OneDayRecentJobsAPIView.as_view(), name='one_day_ago'),

   
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

