from rest_framework import serializers

from apps.base.serializers import AbstractCustomSerializerMixin

class CustomModelSerializer(AbstractCustomSerializerMixin, serializers.ModelSerializer):
    pass
