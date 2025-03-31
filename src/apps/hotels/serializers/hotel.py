from rest_framework import serializers

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

    total_guests_price = serializers.SerializerMethodField()

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
            "total_guests_price"
        ]
        help_texts = {
            "id": "Unique identifier for the hotel.",
            "name": "The name of the hotel.",
            "address": "The physical address of the hotel.",
            "email": "Contact email of the hotel.",
            "phone_number": "Contact phone number of the hotel.",
            "rating": "Hotel rating (0.00 - 5.00).",
        }

    def get_total_guests_price(self, obj):
        guests_data = GuestForHotelOrderSerializer(obj.guests.all(), many=True).data
        return sum(
            guest.get("total_price", 0)
            for guest in guests_data
            if guest.get("total_price") is not None
        )


# {
#     "hotel": "ad72419c-4dd1-4021-aa5d-e46de1257ee1",
#     "order_status": "Active",
#     "room": "e05b85e7-0131-4eca-b157-7917df9bc08e",
#     "guest_details": [
#         {"full_name": "John Maxson", "gender": 1},
#         {"full_name": "Julian", "gender": 1}
#     ],
#     "check_in": "31.03.2025 15:50",
#     "check_out": "5.04.2025 19:50",
#     "count_of_people": 2
# }