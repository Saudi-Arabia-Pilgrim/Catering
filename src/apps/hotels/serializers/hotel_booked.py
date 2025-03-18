from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.hotels.models import Hotel
from apps.rooms.models import Room
from apps.rooms.serializers.room import RoomBookedSerializer


class HotelBookedSerializer(CustomModelSerializer):

    rooms = RoomBookedSerializer(many=True)

    class Meta:
        model = Hotel
        fields = [
            "name",
            "rating",
            "address",
            "rooms"
        ]