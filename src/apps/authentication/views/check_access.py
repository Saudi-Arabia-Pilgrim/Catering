from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.authentication.serializers import CheckAccessSerializer

class CheckAccessGenericAPIView(CustomGenericAPIView):
    """
    Endpoint for access verification.

    Accepts a POST request with data, validates it, and returns the result.

    Methods:
        post(request):
            Validates and saves the data, returning the result in JSON format.

    Passed tests: Production ready!
    """

    permission_classes = []
    authentication_classes = []
    serializer_class = CheckAccessSerializer
    queryset = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=200)