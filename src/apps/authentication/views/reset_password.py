from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.authentication.serializers.reset_password import ResetPasswordSerializer


class ResetPasswordAPIView(APIView):
    """
    API view for resetting a user's password from inside their profile.
    Requires the user to be authenticated.
    """
    permission_classes = [IsAuthenticated]

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