from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.authentication.views import (
    CustomTokenObtainPairView,
    UserLoginView,
    UserLogoutView,
    CheckAccessGenericAPIView,
    ForgotPasswordThroughEmailSendCodeAPIView,
    ForgotPasswordThroughEmailVerifyCodeAPIView,
    ForgotPasswordThroughEmailChangePasswordAPIView,
    ResetPasswordAPIView
)

app_name = 'authentication'

urlpatterns = [
    # JWT Token endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Check access endpoint
    path('check_access/', CheckAccessGenericAPIView.as_view(), name='check_access'),

    # User authentication endpoints
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Forgot password endpoints
    path('forgot-password/email/send-code/', ForgotPasswordThroughEmailSendCodeAPIView.as_view(), name='forgot_password_email_send_code'),
    path('forgot-password/email/verify-code/', ForgotPasswordThroughEmailVerifyCodeAPIView.as_view(), name='forgot_password_email_verify'),
    path('forgot-password/email/set-password/', ForgotPasswordThroughEmailChangePasswordAPIView.as_view(), name='forgot_password_email_new_password'),

    # Reset password endpoint (for authenticated users)
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
]
