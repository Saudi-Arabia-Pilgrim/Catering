# SPECTACULAR_SETTINGS = {
#     'TITLE': 'Catering & Hotels ERP API',
#     'DESCRIPTION': 'An ERP system for managing catering and hotel services for pilgrims during Hajj and Umrah.',
#     'VERSION': '1.0.0',
#     'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
#     'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
#     'REDOC_DIST': 'SIDECAR',
#
#     'SERVE_INCLUDE_SCHEMA': True,
#     'SCHEMA_PATH_PREFIX': '',
#     'SWAGGER_UI_SETTINGS': {
#         'persistAuthorization': True,  # ✅ Makes JWT stick in Swagger
#     },
#     'AUTHENTICATION_WHITELIST': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
#     "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
#     "SERVE_AUTHENTICATION": [
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ],
#
#     # Add JWT token support in Swagger UI
#     "COMPONENT_SPLIT_REQUEST": True,
#     "SECURITY": [{"Bearer": []}],
#     "COMPONENTS": {
#         "securitySchemes": {
#             "Bearer": {
#                 "type": "http",
#                 "scheme": "bearer",
#                 "bearerFormat": "JWT",
#             }
#         }
#     },
# }
#
