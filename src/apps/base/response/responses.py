from rest_framework import status
from rest_framework.response import Response


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
    code = status.HTTP_200_OK

    def __init__(
        self, message='', data=None, status_code: int = None, headers=None, exception=False, content_type=None
    ):
        if status_code is None:
            status_code = self.code

        payload = {"success":True, "message":message, "data":data, }
        super().__init__(
            data=payload, status=status_code, headers=headers, exception=exception, content_type=content_type
        )
