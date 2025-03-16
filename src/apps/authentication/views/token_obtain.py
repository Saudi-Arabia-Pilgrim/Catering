from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.serializers import (
    CustomTokenObtainPairSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that uses the CustomTokenObtainPairSerializer.
    """
    serializer_class = CustomTokenObtainPairSerializer

