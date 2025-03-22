from apps.guests.serializers import GuestSerializer
from apps.hotels.models import Hotel
from apps.base.serializers import CustomModelSerializer
from apps.rooms.serializers.room import RoomSerializer


class HotelSerializer(CustomModelSerializer):
    """
    Serializer for the Hotel model.

    This serializer includes hotel details along with related rooms and guests.
    """

    rooms = RoomSerializer(many=True, help_text="List of rooms associated with the hotel.", read_only=True)
    guests = GuestSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "address",
            "email",
            "phone_number",
            "rating",
            "rooms",
            "guests",
        ]
        help_texts = {
            "id": "Unique identifier for the hotel.",
            "name": "The name of the hotel.",
            "address": "The physical address of the hotel.",
            "email": "Contact email of the hotel.",
            "phone_number": "Contact phone number of the hotel.",
            "rating": "Hotel rating (0.00 - 5.00).",
        }
