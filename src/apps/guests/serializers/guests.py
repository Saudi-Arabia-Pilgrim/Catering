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

    hotel = serializers.CharField(write_only=True)

    class Meta:
        model = Guest
        fields = [
            "id",
            "hotel",
            "full_name",
            "order_number",
            "room_type",
            "gender",
            "check_in",
            "check_out",
            "price",
        ]

    def get_gender(self, obj):
        return obj.get_gender_display()


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
        validated_data["hotel"] = Hotel.objects.get(id=hotel_id)
        return super().create(validated_data)




{
    "hotel": "Taiba Suites Madinah",
    "full_name": "Kimdirov Kimdir",
    "room_type": "2 Kishilik",
    "gender": "Male",
    "check_in": "12.03.2025",
    "check_out": "20.03.2025",
    "price": 120
}
