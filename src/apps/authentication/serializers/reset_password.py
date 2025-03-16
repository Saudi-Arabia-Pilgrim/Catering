from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for resetting a user's password from inside their profile.
    Requires the current password for verification and a new password with confirmation.
    """
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        """
        Validate that the current password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs):
        """
        Validate that the new passwords match.
        """
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "New password fields didn't match."})
        return attrs

    def save(self):
        """
        Set the new password for the user.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        return {'success': True, 'message': 'Password has been reset successfully.'}