from django.core.validators import validate_image_file_extension
from PIL import Image

from apps.base.exceptions import CustomExceptionError


def validate_image_size(image):
    """ Validate image size """

    max_width = 3000
    max_height = 1500

    if not image:
        raise CustomExceptionError(code=400, detail="Provided file is not an image.")

    try:
        validate_image_file_extension(image)

        img = Image.open(image)
        if img.width > max_width or img.height > max_height:
            raise CustomExceptionError(
                code=400, detail=f"Image width and height should be {max_width} and {max_height}"
            )

    except (AttributeError, IOError):
        raise CustomExceptionError(code=400, detail="Invalid image file. Could not open the image.")
