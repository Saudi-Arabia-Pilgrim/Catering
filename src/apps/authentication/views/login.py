import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.tasks import send_email_to_user
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
            # Read the HTML file content
            html_file_path = os.path.join(settings.BASE_DIR, 'config', 'settings', 'emails', 'new_login.html')
            with open(html_file_path, 'r') as file:
                html_content = file.read()

            # Format the HTML content with the RESET_PASSWORD_LINK
            formatted_html = html_content.format(RESET_PASSWORD_LINK=settings.RESET_PASSWORD_LINK)

            send_email_to_user.delay(
                subject="New Login Detected!",
                email=serializer.validated_data["email"],
                message=formatted_html
            )
            return Response(serializer.validated_data, status=200)

        return Response(serializer.errors, status=400)
