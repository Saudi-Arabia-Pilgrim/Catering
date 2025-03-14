from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from apps.base.serializers import EmptySerializer


class BaseThrottle(UserRateThrottle):
    rate = '1000/day'


class BaseAPIView(views.APIView):
    """
    BaseAPIView permissions, throttling.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [BaseThrottle]

    serializer_class = EmptySerializer
    queryset = []


