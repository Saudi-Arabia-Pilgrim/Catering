from apps.guests.serializers.order_guests import GuestForHotelOrderSerializer
from apps.hotels.models import Hotel
from apps.base.serializers import CustomModelSerializer
from apps.rooms.serializers import RoomSerializer


class HotelSerializer(CustomModelSerializer):
    """
    Serializer for the Hotel model.

    This serializer includes hotel details along with related rooms and guests.
    """

    rooms = RoomSerializer(many=True, help_text="List of rooms associated with the hotel.", read_only=True)
    guests = GuestForHotelOrderSerializer(many=True, read_only=True)

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

    def to_representation(self, instance):
        # Optimize the serialization process
        representation = super().to_representation(instance)

        # Access prefetched data efficiently
        representation['rooms'] = RoomSerializer(
            instance.rooms.all(),
            many=True,
            context=self.context
        ).data

        representation['guests'] = GuestForHotelOrderSerializer(
            instance.guests.all(),
            many=True,
            context=self.context
        ).data

        return representation