from django.urls import path

from apps.authentication.views import (
    CustomTokenObtainPairView,
    CheckAccessGenericAPIView,
    CustomTokenRefreshView,
)

app_name = 'authentication'

urlpatterns = [
    # === JWT Token endpoints ===
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # === Check access endpoint ===
    path('check_access/', CheckAccessGenericAPIView.as_view(), name='check_access'),
]
