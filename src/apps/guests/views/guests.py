from django.db.models import Sum
from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.guests.models import Guest
from apps.guests.serializers import GuestSerializer

class HotelGuestListAPIView(CustomGenericAPIView):
    """
    API view to retrieve a list of guests for a specific hotel.

    This view fetches all guests associated with a given hotel ID,
    serializes the data, and returns the total price of all guests.
    """
    serializer_class = GuestSerializer

    def get_queryset(self):
        """
        Retrieve the queryset of guests for the specified hotel.

        Returns:
            QuerySet: Guests belonging to the given hotel.
        """
        hotel_id = self.kwargs.get("hotel_id")
        return Guest.objects.filter(hotel_id=hotel_id)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to return guest data and total price.

        Args:
            request (Request): The request object.

        Returns:
            Response: A response containing the guest list and total price.
        """
        guests = self.get_queryset()
        serializer = self.get_serializer(guests, many=True)

        total_price = guests.aggregate(total=Sum("price"))['total'] or 0

        return Response({
            "guests": serializer.data,
            "total_price": total_price
        })


class AddGuestAPIView(CustomGenericAPIView):
    """
    API view to add a new guest to a specific hotel.

    This view handles POST requests to create a new guest entry
    and associates it with the specified hotel.
    """
    serializer_class = GuestSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new guest.

        Args:
            request (Request): The request object containing guest data.

        Returns:
            Response: A response containing the created guest data or errors.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel_id=self.kwargs.get("hotel_id"))
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
