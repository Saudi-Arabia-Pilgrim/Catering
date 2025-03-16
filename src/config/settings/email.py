import os

from django.conf import settings

from dotenv import load_dotenv

load_dotenv()

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

# Email address to send emails from
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
