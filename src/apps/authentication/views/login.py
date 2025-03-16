from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from apps.authentication.serializers import (
    UserLoginSerializer
)

class UserLoginView(APIView):
    """
    View for user login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': str(user.id),
                'username': user.username,
                'full_name': user.full_name,
                'role': user.role,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
