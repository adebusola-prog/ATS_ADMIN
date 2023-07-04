from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LoginView, LogoutView


app_name = "authe"

urlpatterns = [
    path('login', LoginView.as_view(), name='log_in'), 
    path('logout', LogoutView.as_view(), name='log_out'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

