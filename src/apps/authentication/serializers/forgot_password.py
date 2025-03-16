from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string

User = get_user_model()

class ForgotPasswordEmailSerializer(serializers.Serializer):
    """
    Serializer for sending a verification code to the user's email.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        Validate that the email exists in the database.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value

    def save(self):
        """
        Generate a verification code and send it to the user's email.
        """
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate a random 6-digit code
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        
        # Store the code in the user's session
        self.context['request'].session['password_reset_code'] = code
        self.context['request'].session['password_reset_email'] = email
        
        # Send the code to the user's email
        subject = 'Password Reset Verification Code'
        message = f'Your verification code is: {code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        
        send_mail(subject, message, from_email, recipient_list)
        
        return {'success': True, 'message': 'Verification code sent to your email.'}


class VerifyCodeSerializer(serializers.Serializer):
    """
    Serializer for verifying the code sent to the user's email.
    """
    code = serializers.CharField(required=True)

    def validate_code(self, value):
        """
        Validate that the code matches the one stored in the session.
        """
        stored_code = self.context['request'].session.get('password_reset_code')
        if not stored_code or value != stored_code:
            raise serializers.ValidationError("Invalid verification code.")
        return value

    def save(self):
        """
        Generate a token for password reset and return it.
        """
        email = self.context['request'].session.get('password_reset_email')
        user = User.objects.get(email=email)
        
        # Generate a token for password reset
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # Store the token in the session
        self.context['request'].session['password_reset_uid'] = uid
        self.context['request'].session['password_reset_token'] = token
        
        return {'success': True, 'uid': uid, 'token': token}


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