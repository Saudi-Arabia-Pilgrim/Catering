from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from apps.base.views import CustomModelViewSet
from apps.users.serializers import UserSerializer



class UserViewSet(CustomModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Optionally override this method to customize permission checking,
            or you can specify permission_classes in the class definition.
        :return:
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self):
        return self.request.user

