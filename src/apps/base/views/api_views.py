from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle


class BaseThrottle(UserRateThrottle):
    rate = '1000/day'


class BaseAPIView(views.APIView):
    """
    BaseAPIView permissions, throttling.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [BaseThrottle]

    pass


