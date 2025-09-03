from rest_framework import serializers
# from django.conf import settings

# from apps.base.exceptions.exception_error import CustomExceptionError


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
    
    # def to_representation(self, instance):
    #     request = self.context.get("request", None)
    #     translation_fields = getattr(instance, "translation_fields", None)
    #     data = super().to_representation(instance)

    #     if not translation_fields or not request:
    #         return data

    #     default_lang = settings.MODELTRANSLATION_DEFAULT_LANGUAGE
    #     languages = [lang[0] for lang in settings.LANGUAGES]
    #     lang = request.query_params.get('lang', default_lang)

    #     if lang not in languages:
    #         lang = default_lang

    #     for field_name in translation_fields:
    #         data[field_name] = getattr(instance, f"{field_name}_{lang}")
    #         for lang in languages:
    #             data.pop(f"{field_name}_{lang}")

    #     return data

    # def to_internal_value(self, data):
    #     data = super().to_internal_value(data)
    #     required_fields = getattr(self.Meta, "required_fields", None)
        
    #     if not required_fields:
    #         return data

    #     for field in required_fields:
    #         if field in data and not str(data[field]).strip():
    #             raise CustomExceptionError(code=400, detail=f"The field '{field}' is required and cannot be empty.")
        
    #     return data