from django.db.models import Sum
from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.guests.models import Guest
from apps.guests.serializers import GuestSerializer
from apps.rooms.models import Room
from apps.rooms.serializers import RoomSerializer


class HotelStatsAPIView(CustomGenericAPIView):
    """
    API view to retrieve hotel statistics, including guest and room data.

    This view provides aggregated analytics for a given hotel, including:
    - List of guests and total guest revenue
    - List of rooms and total room revenue
    - Overall total revenue (sum of guest and room prices)

    Inherits from:
        CustomGenericAPIView: A customized generic API view.

    Methods:
        get(request, pk, *args, **kwargs): Handles GET requests and returns hotel statistics.
    """

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve statistical data for a specific hotel.

        Args:
            request (HttpRequest): The request object.
            pk (int): The primary key (ID) of the hotel.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response (dict): A dictionary containing:
                - "guests": Serialized list of guests.
                - "total_guest_price": Total price for all guests.
                - "rooms": Serialized list of rooms.
                - "total_rooms_price": Total price for all rooms.
                - "total_price": The overall total revenue (guest + room prices).
        """
        # Guests Analytics
        guest_queryset = Guest.objects.filter(hotel_id=pk)
        total_guest_price = guest_queryset.aggregate(total=Sum("price"))["total"] or 0
        guest_serializer = GuestSerializer(guest_queryset, many=True)

        # Rooms Analytics
        room_queryset = Room.objects.filter(hotel_id=pk)
        total_rooms_price = room_queryset.aggregate(total=Sum("price"))["total"] or 0
        room_serializer = RoomSerializer(room_queryset, many=True)

        # General Price
        total_price = total_guest_price + total_rooms_price

        return Response({
            "guests": guest_serializer.data,
            "total_guest_price": total_guest_price,
            "rooms": room_serializer.data,
            "total_rooms_price": total_rooms_price,
            "total_price": total_price
        })
