from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that adds user information to the token response.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['full_name'] = user.full_name
        token['role'] = user.role
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra responses
        data['user_id'] = str(self.user.id)
        data['email'] = self.user.email
        data['full_name'] = self.user.full_name
        data['role'] = self.user.role
        data['is_staff'] = self.user.is_staff
        data['is_superuser'] = self.user.is_superuser

        return data
