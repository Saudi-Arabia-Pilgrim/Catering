from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.authentication.serializers.forgot_password import (
    ForgotPasswordEmailSerializer,
    VerifyCodeSerializer,
    SetNewPasswordSerializer
)


class ForgotPasswordThroughEmailSendCodeAPIView(APIView):
    """
    API view for sending a verification code to the user's email for password reset.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Send a verification code to the user's email.
        """
        serializer = ForgotPasswordEmailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordThroughEmailVerifyCodeAPIView(APIView):
    """
    API view for verifying the code sent to the user's email for password reset.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Verify the code sent to the user's email.
        """
        serializer = VerifyCodeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordThroughEmailChangePasswordAPIView(APIView):
    """
    API view for setting a new password after verifying the code.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Set a new password for the user.
        """
        serializer = SetNewPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)