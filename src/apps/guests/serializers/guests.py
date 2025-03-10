from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.guests.models import Guest


class GuestSerializer(CustomModelSerializer):
    """
    Serializer for the Guest model.

    This serializer handles guest-related data, including retrieving guest details
    and creating new guest entries with an associated hotel.
    """

    hotel = serializers.SerializerMethodField(help_text="Name of the hotel associated with the guest.")

    class Meta:
        model = Guest
        fields = [
            "id",  # Unique identifier for the guest.
            "hotel",  # The name of the hotel associated with the guest.
            "gender",  # Gender of the guest.
            "full_name",  # Full name of the guest.
            "price",  # Price associated with the guest's stay.
        ]

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
        validated_data["hotel_id"] = hotel_id
        return super().create(validated_data)

    def get_hotel(self, obj):
        """
        Retrieve the name of the hotel associated with the guest.

        Args:
            obj (Guest): Guest instance.

        Returns:
            str: Name of the associated hotel.
        """
        return obj.hotel.name