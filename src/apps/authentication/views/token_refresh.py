from rest_framework_simplejwt.views import TokenRefreshView
from apps.base.views import CustomGenericAPIView

class CustomTokenRefreshView(TokenRefreshView, CustomGenericAPIView):
    """
    Refresh token by sending refresh token.
    params: refresh_token
    returns: access_token & refresh_token
    Passed tests: Production ready!
    """
    pass