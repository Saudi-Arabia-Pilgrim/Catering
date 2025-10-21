import uuid

from apps.base.exceptions.exception_error import CustomExceptionError

def validate_uuid(uid: str) -> bool:
    """
    Validates if the given string is a valid UUID.

    Args:
        uid (str): The string to validate.

    Returns:
        bool: True if the string is a valid UUID, False otherwise.
    """
    try:
        uuid_obj = uuid.UUID(uid)
        return str(uuid_obj) == uid
    except ValueError:
        raise CustomExceptionError(code=400, detail="Invalid UUID format.")