from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    LoginView,
    ForgotPasswordView,
    ResetPasswordView,
    SetNewPasswordView,
    PermissionLevelListAPIView,
#     LogoutView,
)

app_name = "authe"

urlpatterns = [
        path('permission_level', PermissionLevelListAPIView.as_view(), name='permission_level'),    
        path('login', LoginView.as_view(), name='log_in'), 
        # path('logout', LogoutView.as_view(), name='log_out'),
        path('forgot_password', ForgotPasswordView.as_view(),\
                name='forgot_password'),
        path('reset_password/<str:uuidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
        path('password_reset_complete', SetNewPasswordView.as_view(), name='password_reset_complete'),
            
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

