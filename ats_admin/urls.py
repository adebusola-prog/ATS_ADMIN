from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SuperAdminDetailView, ProfilePictureUpdateView, SubAdminCreateView,\
      SubAdminListView


app_name = "ats"

urlpatterns = [
    path('superadmin/', SuperAdminDetailView.as_view(), name='superadmin_detail'), 
    path('profile_picture/', ProfilePictureUpdateView.as_view(), name='profile_picture_update'),
    path('create_sub_admin', SubAdminCreateView.as_view(), name='create_sub_admin'),
    path('sub_admin_list', SubAdminListView.as_view(), name="sub_admin_list")
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

