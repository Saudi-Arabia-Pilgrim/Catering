from rest_framework import status
from rest_framework.response import Response
from apps.base.views import CustomGenericAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample

from apps.users.serializers import (
    ForgotPasswordSendEmailSerializer,
    VerifyCodeSerializer,
    SetNewPasswordSerializer
)

class ForgotPasswordThroughEmailSendCodeAPIView(CustomGenericAPIView):
    """
    API view for sending a verification code to the user's email for password reset.
    """
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSendEmailSerializer

    def post(self, request):
        """
        Send a verification code to the user's email.
        """
        serializer = ForgotPasswordSendEmailSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordThroughEmailVerifyCodeAPIView(CustomGenericAPIView):
    """
    API view for verifying the code sent to the user's email for password reset.
    """
    permission_classes = [AllowAny]
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        """
        Verify the code sent to the user's email.
        """
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordThroughEmailChangePasswordAPIView(CustomGenericAPIView):
    """
    API view for setting a new password after verifying the code.
    """
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        """
        Set a new password for the user.
        """
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

