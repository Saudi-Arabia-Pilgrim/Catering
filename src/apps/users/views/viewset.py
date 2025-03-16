from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from apps.base.views import CustomModelViewSet
from apps.users.serializers import UserSerializer
from apps.users.permissions import RoleBasedPermission


class UserViewSet(CustomModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    department = 'users'  # This is used by RoleBasedPermission

    def get_permissions(self):
        """
        Use both IsAuthenticated and RoleBasedPermission for permission checking.
        :return:
        """
        permission_classes = [IsAuthenticated, RoleBasedPermission]
        return [permission() for permission in permission_classes]

    def get_object(self):
        """
        If the action is 'me', return the current user.
        Otherwise, use the default behavior.
        """
        if self.action == 'me':
            return self.request.user
        return super().get_object()

    def get_queryset(self):
        """
        Filter the queryset based on the user's role.
        Superusers and admins can see all users.
        Other users can only see themselves.
        """
        user = self.request.user
        if user.is_superuser or user.role == 'admin':
            return self.queryset
        return self.queryset.filter(id=user.id)
