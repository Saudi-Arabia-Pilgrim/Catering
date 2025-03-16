from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from apps.base.serializers import CustomModelSerializer


class UserSerializer(CustomModelSerializer):
    """
    Serializer for custom user model
    """
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'full_name', 'birthdate', 'gender',
            'role', 'is_active', 'is_staff', 'is_superuser'
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
        }

    async def create(self, validated_data):
        create_user = sync_to_async(get_user_model().objects.create_user)
        return await create_user(**validated_data)

    async def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        update_user = sync_to_async(super().update)
        user = await update_user(instance, validated_data)
        if password:
            set_password = sync_to_async(user.set_password)
            await set_password(password)
            save_user = sync_to_async(user.save)
            await save_user()
        return user
