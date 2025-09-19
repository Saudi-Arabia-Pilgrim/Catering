from apps.base.views import CustomListAPIView, CustomCreateAPIView, CustomRetrieveUpdateAPIView, \
    CustomDestroyAPIView
from apps.guests.models import GuestGroup
from apps.guests.serializers.group_guests import (GuestGroupListSerializer,
                                                  GuestGroupRetrieveUpdateSerializer,
                                                  GuestGroupDeleteSerializer,
                                                  GuestGroupCreateSerializer)


class GuestGroupListAPIView(CustomListAPIView):
    queryset = GuestGroup.objects.all()
    serializer_class = GuestGroupListSerializer


class GuestGroupCreateAPIView(CustomCreateAPIView):
    queryset = GuestGroup.objects.all()
    serializer_class = GuestGroupCreateSerializer


class GuestGroupRetrieveUpdateAPIView(CustomRetrieveUpdateAPIView):
    queryset = GuestGroup.objects.all()
    serializer_class = GuestGroupRetrieveUpdateSerializer


class GuestGroupDeleteAPIView(CustomDestroyAPIView):
    queryset = GuestGroup.objects.all()
    serializer_class = GuestGroupDeleteSerializer
