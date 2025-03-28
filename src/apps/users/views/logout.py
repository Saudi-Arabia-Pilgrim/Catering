from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class UserLogoutView(APIView):
    """
    View for user logout.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={'type': 'object', 'properties': {'refresh': {'type': 'string'}}},
        responses={205: None},
        description="Logout by blacklisting the refresh token.",
        examples=[
            OpenApiExample(
                'Logout Example',
                value={'refresh': 'your-refresh-token'},
                request_only=True,
            ),
        ]
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
