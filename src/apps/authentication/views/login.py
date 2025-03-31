from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.base.views import CustomGenericAPIView
from apps.authentication.serializers import (
    CustomTokenObtainPairSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView, CustomGenericAPIView):
    """
    API endpoint for login.
    params: username, password
    returns: token, refresh_token
    """
    permission_classes = []
    authentication_classes = []

    serializer_class = CustomTokenObtainPairSerializer

    queryset = []

    def post(self, request, *args, **kwargs):
        """
        Custom post method to handle the token generation.
        """
        serializer = CustomTokenObtainPairSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=200)

        return Response(serializer.errors, status=400)
