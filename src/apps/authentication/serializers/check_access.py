from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rest_framework_simplejwt.tokens import AccessToken

from apps.base.serializers import CustomSerializer
from apps.base.exceptions import CustomExceptionError


class CheckAccessSerializer(CustomSerializer):
    """
    CheckAccessSerializer is responsible for validating the access token and determining
    whether the user has access. It extends the CustomSerializer class and includes the
    following fields:
    Attributes:
        access_token (serializers.CharField): The access token provided by the user.
        access (serializers.BooleanField): A read-only field indicating whether the user has access.
    Methods:
        save(**kwargs):
            Validates the access token and retrieves the associated user. If the token is invalid
            or the user is not found, raises a CustomAPIExceptionError. Sets the 'access' field to
            True if the token is valid and deletes the 'access_token' from the validated data.
    """

    access_token = serializers.CharField()

    def save(self, **kwargs):
        try:
            token = AccessToken(self.validated_data["access_token"])
            user = get_user_model().objects.get(id=token["user_id"])
            if not user:
                raise CustomExceptionError(code=404, detail=_("User not found"))
        except Exception as e:
            raise CustomExceptionError(code=400, detail=_("This token is not valid"))
        self.validated_data['access'] = True
        del self.validated_data['access_token']
