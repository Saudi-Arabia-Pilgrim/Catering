from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from apps.authentication.serializers import (
    CustomTokenObtainPairSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that uses the CustomTokenObtainPairSerializer.
    """
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        request={'type': 'object', 'properties': {'email': {'type': 'string'}, 'password': {'type': 'string'}}},
        responses={200: dict},
        description="Obtain JWT token pair (access and refresh tokens) by providing email and password.",
        examples=[
            OpenApiExample(
                'Token Obtain Example',
                value={'email': 'user@example.com', 'password': 'yourpassword'},
                request_only=True,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
