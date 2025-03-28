from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample

from apps.users.serializers.reset_password import ResetPasswordSerializer


class ResetPasswordAPIView(APIView):
    """
    API view for resetting a user's password from inside their profile.
    Requires the user to be authenticated.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: dict},
        description="Reset the user's password. Requires the current password for verification and a new password with confirmation.",
        examples=[
            OpenApiExample(
                'Reset Password Example',
                value={
                    'current_password': 'currentpassword',
                    'new_password': 'newpassword123',
                    'new_password2': 'newpassword123'
                },
                request_only=True,
            ),
        ]
    )
    def post(self, request):
        """
        Reset the user's password.
        Requires the current password for verification and a new password with confirmation.
        """
        serializer = ResetPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
