from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from apps.base.serializers import CustomSerializer

User = get_user_model()

class ResetPasswordSerializer(CustomSerializer):
    """
    Serializer for resetting a user's password from inside their profile.
    Requires the current password for verification and a new password with confirmation.
    """
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

    # JWT token fields that will be returned after password reset
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def validate_current_password(self, value):
        """
        Validate that the current password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")

        # Revoke all existing tokens for the user to ensure old tokens are invalidated
        User.revoke_user_tokens(user)

        return value

    def save(self):
        """
        Set the new password for the user.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

        # Generate new JWT tokens for the user after password change
        refresh = RefreshToken.for_user(user)

        # Add the new tokens to the validated data
        self.validated_data["refresh"] = str(refresh)
        self.validated_data["access"] = str(refresh.access_token)

        # Remove sensitive password data from validated_data
        del self.validated_data["current_password"]
        del self.validated_data["new_password"]
        
        return {'success': True, 'message': 'Password has been reset successfully.'}

