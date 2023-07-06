from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import JobListCreateAPIView, JobDetailUpdateAPIView,\
      JobApplicantCreateAPIView, JobDeleteAPIView, JobApplicantDetailAPIView,\
      JobApplicantListAPIView


app_name = "jobs"

urlpatterns = [
    path('job_list_create', JobListCreateAPIView.as_view(), name='job_list_create'), 
    path('<int:pk>/job_detail_update', JobDetailUpdateAPIView.as_view(), name='job_detail_update'),
    path('<int:pk>/job_delete', JobDeleteAPIView.as_view(), name='job_delete'),
    path('job_application_create', JobApplicantCreateAPIView.as_view(), name='job_application_create'),
    path('job_application_list', JobApplicantListAPIView.as_view(), name='job_application_list'),
    path('job_application_detail', JobApplicantDetailAPIView.as_view(), name='job_application_detail')
  
   
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

