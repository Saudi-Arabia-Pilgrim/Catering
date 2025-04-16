from rest_framework.response import Response
from rest_framework import status


class CustomSuccessResponse(Response):
    """
    A custom Response class for success responses that returns a consistent structure.
    The response will have a structure like:

      {
          "success": True,
          "message": "Your human-readable message here",
          "data": { ... }  # the data payload
      }
    """

    def __init__(
        self, message='', data=None, status_code=status.HTTP_200_OK, headers=None, exception=False, content_type=None
    ):
        payload = {"success":True, "message":message, "data":data, }
        super().__init__(
            data=payload, status=status_code, headers=headers, exception=exception, content_type=content_type
        )
