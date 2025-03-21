from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.guests.models import Guest
from apps.hotels.models import Hotel


class GuestSerializer(CustomModelSerializer):
    """
    Serializer for the Guest model.

    This serializer handles guest-related data, including retrieving guest details
    and creating new guest entries with an associated hotel.
    """
    room_type = serializers.CharField(source="room.room_type", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Guest
        fields = [
            "full_name",
            "order_number",
            "room",
            "room_type",
            "gender",
            "check_in",
            "check_out",
            "total_price"
        ]
        read_only_fields = ["order_number", "price", "room_type"]

    def get_total_price(self, obj):
        if obj.check_in and obj.check_out and obj.room:
            days_stayed = (obj.check_out - obj.check_in).days
            if days_stayed < 1:
                days_stayed = 1
            return obj.room.gross_price * days_stayed
        return 0

    def create(self, validated_data):
        """
        Create a new Guest instance.

        Automatically assigns the hotel based on the `hotel_id` extracted from the view context.

        Args:
            validated_data (dict): Validated data for creating a Guest instance.

        Returns:
            Guest: Newly created Guest instance.
        """
        hotel_id = self.context["view"].kwargs.get("hotel_id")
        if hotel_id:
            validated_data["hotel"] = Hotel.objects.get(id=hotel_id)
        return super().create(validated_data)




# {
#     "hotel": "Taiba Suites Madinah",
#     "full_name": "Kimdirov Kimdir",
#     "room_type": "2 Kishilik",
#     "gender": "Male",
#     "check_in": "12.03.2025",
#     "check_out": "20.03.2025",
#     "price": 120
# }
