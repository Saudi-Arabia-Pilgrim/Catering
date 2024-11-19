# id_utils.py
import random
import string
from typing import Dict
from apps.base.exceptions import CustomExceptionError


class IDGenerationError(CustomExceptionError):
    """Custom exception for ID generation errors"""

    def __init__(self, message: str):
        super().__init__(
            code=400, detail={'error':message}
        )


class SimpleIDGenerator:
    """
    Simple utility for generating and validating 8-character alphanumeric IDs
    """

    @staticmethod
    def generate_id(length: int = 8) -> str:
        """
        Generate a unique alphanumeric ID of specified length.
        Args:
            length (int): Length of the ID to generate (default: 8)
        Returns:
            str: Generated unique ID
        Raises:
            IDGenerationError: If length is invalid
        """
        if length < 1:
            raise IDGenerationError("ID length must be greater than 0")

        # ======== Use uppercase letters, lowercase letters, and digits for more readability ========
        characters = string.ascii_uppercase+string.ascii_lowercase+string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def validate_id(value: str, required_length: int = 8) -> Dict:
        """
        Validate the generated ID.
        Args:
            value (str): ID to validate
            required_length (int): Expected length of the ID
        Returns:
            Dict: Validation result
        Raises:
            IDGenerationError: If ID is invalid
        """

        # ========= Check length ========
        if len(value) != required_length:
            raise IDGenerationError(
                f"ID must be exactly {required_length} characters long"
            )

        # ======== Check character set (alphanumeric) ========
        valid_chars = set(string.ascii_letters+string.digits)
        if not all(char in valid_chars for char in value):
            raise IDGenerationError(
                "ID must contain only letters and numbers"
            )

        return {'message':'Valid ID', 'value':value}

#
# # Optional: Example usage and testing
# if __name__ == "__main__":
#     try:
#         # Generate an ID
#         new_id = SimpleIDGenerator.generate_id()
#         print(f"Generated ID: {new_id}")
#
#         # Validate the ID
#         validation_result = SimpleIDGenerator.validate_id(new_id)
#         print(f"Validation Result: {validation_result}")
#
#     except IDGenerationError as e:
#         print(f"Error: {e.detail['error']}")