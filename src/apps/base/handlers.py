from django.db.models import ProtectedError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Return response if error is Protected"""
    if isinstance(exc, ProtectedError):
        return Response(
            {
                'code':423,
                "detail": "This object cannot be deleted because it is referenced by other objects."
            },
        )
    return exception_handler(exc, context)