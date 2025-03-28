from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.authentication.views import (
    CustomTokenObtainPairView,
    CheckAccessGenericAPIView,
)

app_name = 'authentication'

urlpatterns = [
    # JWT Token endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Check access endpoint
    path('check_access/', CheckAccessGenericAPIView.as_view(), name='check_access'),
]
