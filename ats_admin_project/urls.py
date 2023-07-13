"""ats_admin_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for house_rent_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# from accounts.views import CustomUserDocumentView


# schema_view = get_schema_view(
#     openapi.Info(
#         title="ATS ADMIN",
#         default_version='v1',
#         description="An API Showing ATS ADMIN Features ",
#         terms_of_service="https://www.spoti.com/policies/terms/",
#         contact=openapi.Contact(email="contact@spoti.com",),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
    # permission_classes=[permissions.AllowAny],
# )
# router = routers.SimpleRouter(trailing_slash=False)
# router.register(r'name-search', CustomUserDocumentView, basename='name-search')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('accounts.urls', namespace="authe")),
    path("api/ats_admin/", include("ats_admin.urls", namespace="ats")),
    path("api/job/", include('job.urls', namespace='jobs')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
   
    # path('schema', schema_view.with_ui('swagger',
    #                              cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc',
    #                                    cache_timeout=0), name='schema-redoc'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += router.urls

