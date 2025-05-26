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
        description="API documentation for Catering Project 🚀"
                    "👋 Dear Frontend Team, Please, we *beg you*,"
                    " take a moment to read the **docstrings** we’ve written just for you."
                    " We’ve spent time documenting every field, every serializer, and every view — *not for the backend gods*,"
                    " but so you won’t get stuck with `500 errors` and blame us 😎 📌 Why should you read the docstrings - ❓ What parameters are required - "
                    "🔍 How can you filter data - 🧾 Which fields are optional? Which are mandatory - 📅 What date format is expected? 🎁 It’s all here. Nicely written."
                    " Kindly documented. Just scroll a little. We promise it won’t bite. It might even save you a few hours of debugging. Cheers 🍻 — Your friendly neighborhood Backend Team",
        contact=openapi.Contact(email="https://t.me/mukhsin_mukhtariy"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    url=swagger_base_url,
    authentication_classes=[],
    generator_class=BothHttpAndHttpsSchemaGenerator,
)