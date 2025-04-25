import os

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


# ======== Custom generator to add Bearer security globally ========
class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.security = [{'Bearer': []}]  # 👈 This makes Swagger use Bearer by default
        return schema


# ======== Pick the correct URL for Swagger depending on ENV ========
if settings.NGROK or settings.ENV == "production":
    swagger_base_url = os.getenv("SWAGGER_DOCS_BASE_URL", "https://catering.mukhsin.space")
    print(f"Swagger URL: {swagger_base_url}")
else:
    swagger_base_url = "http://localhost:8000/"


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
    url=swagger_base_url,
    authentication_classes=[],
    generator_class=BothHttpAndHttpsSchemaGenerator,
)