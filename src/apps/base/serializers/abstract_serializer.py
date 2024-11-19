from rest_framework import serializers

class AbstractCustomSerializerMixin:
    """
    A base mixin to be used for custom serialization behaviors in DRF serializers.
    Include common validations, transformations, and error handling that apply broadly across your serializers.
    """

    def validate_positive_number(self, value):
        """
        Validates that a given value is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("This field must be a positive number.")
        return value

    def get_user_from_context(self):
        """Retrieve and return the user from the serializer context."""
        user = self.context['request'].user
        return user if user.is_authenticated else None

    def create(self, validated_data):
        """Handle the creation of a new instance with user context."""
        user = self.get_user_from_context()
        if user:
            validated_data['created_by'] = validated_data['updated_by'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update an existing instance with user context."""
        user = self.get_user_from_context()
        if user:
            validated_data['updated_by'] = user
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        """Custom save method to inject user data on creation or update."""
        user = self.get_user_from_context()
        if user:
            # Directly manipulate kwargs for created_by only if it's a new instance
            if self.instance is None:
                kwargs['created_by'] = user
            kwargs['updated_by'] = user
        return super().save(**kwargs)