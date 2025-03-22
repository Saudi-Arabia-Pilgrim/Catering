from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, UserProfileAPIView

from apps.users.views import (
    UserLogoutView,
    ForgotPasswordThroughEmailSendCodeAPIView,
    ForgotPasswordThroughEmailVerifyCodeAPIView,
    ForgotPasswordThroughEmailChangePasswordAPIView,
    ResetPasswordAPIView
)

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),


    # User authentication endpoints
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Forgot password endpoints
    path('forgot-password/email/send-code/', ForgotPasswordThroughEmailSendCodeAPIView.as_view(), name='forgot_password_email_send_code'),
    path('forgot-password/email/verify-code/', ForgotPasswordThroughEmailVerifyCodeAPIView.as_view(), name='forgot_password_email_verify'),
    path('forgot-password/email/set-password/', ForgotPasswordThroughEmailChangePasswordAPIView.as_view(), name='forgot_password_email_new_password'),

    # Reset password endpoint (for authenticated users)
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
]
