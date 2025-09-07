from django.conf import settings

SPECTACULAR_SETTINGS = {
    'TITLE': 'Catering API',
    'DESCRIPTION': 'API documentation for Catering Project 🚀',
    'VERSION': 'v1',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVERS': [
        {"url": "https://api.maqom360.com"} if settings.NGROK or settings.ENV == "production"
        else {"url": "http://localhost:8000"}
    ],
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [{'BearerAuth': []}],
    'SECURITY_SCHEMES': {
        'BearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"',
        }
    },
}