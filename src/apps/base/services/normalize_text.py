from django.db.models import CharField, Model, TextField


def normalize_text_fields(instance: Model):
    """
    Normalize text fields in the given model instance by stripping leading and trailing whitespace.

    :param instance: The model instance to normalize.
    """
    for field in instance._meta.get_fields():
        if isinstance(field, (CharField, TextField)) and field.editable:
            value = getattr(instance, field.name, None)
            if isinstance(value, str):
                normalized_value = value.strip()
                setattr(instance, field.name, normalized_value)
