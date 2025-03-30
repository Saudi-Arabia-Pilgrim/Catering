from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
import os

# ======== Pick the correct URL for Swagger depending on ENV ========
if settings.NGROK:
    swagger_base_url = os.getenv("SWAGGER_DOCS_BASE_URL", "https://catering.com")
    print(f"Swagger URL: {swagger_base_url}")  # For production, set this in .env file
else:
    swagger_base_url = None  # Uses current localhost (no problem)


# ======== Swagger/OpenAPI schema view ========
schema_view = get_schema_view(
    openapi.Info(
        title="Catering API",
        default_version="v1",
        description="API documentation for Catering Project 🚀",
        contact=openapi.Contact(email="https://t.me/mukhsin_mukhtariy"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    url=swagger_base_url  # 🔁 This auto-switches between local/prod
)

