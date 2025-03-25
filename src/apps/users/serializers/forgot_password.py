import string
import secrets

from django.conf import settings
from django.core.cache import cache
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from apps.users.tasks import send_email_to_user
from apps.base.serializers import CustomSerializer
from apps.base.exceptions import CustomExceptionError

User = get_user_model()

FORGOT_PASSWORD_KEY = "forgot_password_key{email}"
PASSWORD_RESET_UUID = "password_reset_uuid"
PASSWORD_RESET_TOKEN = "password_reset_token"

EMAIL = settings.

class ForgotPasswordSendEmailSerializer(CustomSerializer):
    """
    Serializer for sending a verification code to the user's email.
    """
    email = serializers.EmailField(required=True)
    sended = serializers.BooleanField(read_only=True)


    def validate_email(self, email):
        """
        Validate that the email exists in the database.
        """
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return email

    def save(self):
        """
        Generate a verification code and send it to the user's email.
        Store the code and email in Redis with a timeout (e.g. 10 minutes).
        """
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate a random 6-digit code
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        
        # Send the code to the user's email
        subject = 'Password Reset Verification Code'
        message = settings.VERIFY_CODE_HTML.format(code=code)

        send_email_to_user.delay(subject=subject, email=email, message=message)
        
        # Store the code in the redis
        cache.set(FORGOT_PASSWORD_KEY.format(email=email), code, timeout=60 * 10)
        
        return {'success': True, 'message': 'Verification code sent to your email.'}


class VerifyCodeSerializer(CustomSerializer):
    """
    Serializer for verifying the code sent to the user's email.
    """
    email = serializers.EmailField()
    code = serializers.IntegerField()
    verified = serializers.BooleanField(read_only=True)
    
    def validate(self, attrs):
        if not get_user_model().objects.filter(email=attrs['email']).exists():
            raise CustomExceptionError(_('User with this email does not exist!'))

    def validate_code(self, code):
        """
        Validate that the code matches the one stored in the Redis for the current USER!.
        """
        stored_code = cache.get(FORGOT_PASSWORD_KEY.find(code))
        if not stored_code or code != stored_code:
            raise serializers.ValidationError("Invalid verification code.")
        return code

    def save(self):
        """
        Generate a token for password reset and return it.
        Once the code is used, delete it (and the email) from Redis so it can be used only once.
        """
        email = cache.get(FORGOT_PASSWORD_KEY)
        if not email:
            raise serializers.ValidationError("Verification session has expired or invalid.")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        
        # Generate a token for password reset
        uuid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # Store the uuid & token in Redis for later use (e.g. 5 minutes)
        cache.set(PASSWORD_RESET_UUID, uuid, timeout=60 * 5)
        cache.set(PASSWORD_RESET_TOKEN, token, timeout=60 * 5)

        # === Delete the verification code and email from Redis so they can't be reused. ===
        cache.delete(EMAIL_VERIFY_CODE)
        cache.delete(FORGOT_PASSWORD_EMAIL)

        
        return {'success': True, 'uid': uuid, 'token': token}


class SetNewPasswordSerializer(serializers.Serializer):
    """
    Serializer for setting a new password.
    """
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        Validate that the passwords match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def save(self):
        """
        Set the new password for the user using uid and token stored in Redis. 
        Clears the uid and token from Redis after successful password reset.
        """
        uid = cache.get(PASSWORD_RESET_UUID)
        token = cache.get(PASSWORD_RESET_TOKEN)
        
        if not uid or not token:
            raise serializers.ValidationError("Invalid or expired password reset session.")
        
        try:
            # Decode the user ID
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            
            # Verify the token
            if not default_token_generator.check_token(user, token):
                raise serializers.ValidationError("Invalid reset token.")
            
            # Set the new password
            user.set_password(self.validated_data['password'])
            user.save()
            
            # Clear uid and token from Redis
            cache.delete(PASSWORD_RESET_UUID)
            cache.delete(PASSWORD_RESET_TOKEN)
            
            return {'success': True, 'message': 'Password has been reset successfully.'}
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid reset token.")
        