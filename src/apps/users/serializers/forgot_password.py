from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
import secrets
import string

User = get_user_model()

EMAIL_VERIFY_CODE = "email_verify_code"
FORGOT_PASSWORD_EMAIL = "forgot_password_email"
PASSWORD_RESET_UUID = "password_reset_uuid"
PASSWORD_RESET_TOKEN = "password_reset_token"

class ForgotPasswordEmailSerializer(serializers.Serializer):
    """
    Serializer for sending a verification code to the user's email.
    """
    email = serializers.EmailField(required=True)


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
        
        # Store the code in the redis
        cache.set(EMAIL_VERIFY_CODE, code, timeout=60 * 10)
        cache.set(FORGOT_PASSWORD_EMAIL, email, timeout=60 * 10)
        
        # Send the code to the user's email
        subject = 'Password Reset Verification Code'
        message = (f'Your verification code is: {code}'
                   f"If you didn't request this, please ignore this email!"
                   f"DON'T give away the code to ANYBODY, Be aware of Scammers!")
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        
        send_mail(subject, message, from_email, recipient_list)
        
        return {'success': True, 'message': 'Verification code sent to your email.'}


class VerifyCodeSerializer(serializers.Serializer):
    """
    Serializer for verifying the code sent to the user's email.
    """
    class Meta:
        code = serializers.CharField(required=True)

    def validate_code(self, value):
        """
        Validate that the code matches the one stored in the Redis.
        """
        stored_code = cache.get(EMAIL_VERIFY_CODE)
        if not stored_code or value != stored_code:
            raise serializers.ValidationError("Invalid verification code.")
        return value

    def save(self):
        """
        Generate a token for password reset and return it.
        Once the code is used, delete it (and the email) from Redis so it can be used only once.
        """
        email = cache.get(FORGOT_PASSWORD_EMAIL)
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

        # === Delete the

        
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
        Set the new password for the user.
        """
        uid = self.context['request'].session.get('password_reset_uid')
        token = self.context['request'].session.get('password_reset_token')
        
        if not uid or not token:
            raise serializers.ValidationError("Invalid password reset session.")
        
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
            
            # Clear the session
            self.context['request'].session.pop('password_reset_code', None)
            self.context['request'].session.pop('password_reset_email', None)
            self.context['request'].session.pop('password_reset_uid', None)
            self.context['request'].session.pop('password_reset_token', None)
            
            return {'success': True, 'message': 'Password has been reset successfully.'}
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid reset token.")