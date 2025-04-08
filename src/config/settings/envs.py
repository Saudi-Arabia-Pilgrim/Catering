import os

from dotenv import load_dotenv

load_dotenv()


# ===================== REDIS configurations =====================
REDIS_PORT_URL = os.getenv('REDIS_PORT_URL')

# ===================== Swagger dynamic configurations =====================
SWAGGER_DOCS_BASE_URL=os.getenv("SWAGGER_DOCS_BASE_URL", "https://catering.com")
NGROK = os.getenv("NGROK", False)

# ===================== Django configurations =====================
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
TIME_ZONE = os.getenv("TIME_ZONE")
USE_I18N = os.getenv("USE_I18N")
USE_L10N = os.getenv("USE_L10N")
USE_TZ = os.getenv("USE_TZ")


# ===================== Company Email Message configurations =====================
RESET_PASSWORD_LINK=os.getenv("RESET_PASSWORD_LINK")

ENV = os.getenv("ENV")

# ===================== JWT configurations =====================
PRIVATE_KEY = open('./config/secrets/private.pem').read()
PUBLIC_KEY = open('./config/secrets/public.pem').read()

