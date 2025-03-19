from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.guests.serializers import GuestSerializer
from apps.orders.models import HotelOrder


class AddGuestToHotelOrderAPIView(CustomGenericAPIView):
    serializer_class = GuestSerializer

    def post(self, request, order_id, *args, **kwargs):
        try:
            hotel_order = HotelOrder.objects.get(id=order_id)
        except HotelOrder.DoesNotExists:
            return Response({"detail": "HotelOrder not found."}, status=404)

        guests_data = request.data.get("guests", [])
        created_guests = []

        for guest_data in guests_data:
            guest_data["hotel_order"] = hotel_order.id
            guest_data["hotel"] = hotel_order.hotel.id

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            guest = serializer.save()

            hotel_order.guests.add(guest)
            created_guests.append(serializer.data)

        return Response(
            {"order_id": hotel_order.id, "created_guests": created_guests},
            status=201
        )
