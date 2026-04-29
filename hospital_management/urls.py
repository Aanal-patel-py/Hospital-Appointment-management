

from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from Users import views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Hospital API",
        default_version='v1',
        description="API documentation for Hospital Appointment System",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    # path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('',include('Users.urls')),
    path('',include('Doctor.urls')),
    path('',include('Patient.urls')),
    path('',include('Appointments.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    ]
