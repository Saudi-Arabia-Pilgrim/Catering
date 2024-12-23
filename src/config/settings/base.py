import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()



BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
print("Secret Key: ", SECRET_KEY)
SIGNING_KEY = os.getenv("SIGNING_KEY")
DEBUG = os.getenv("DEBUG")
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
print("Allowed Hosts:", ALLOWED_HOSTS)
REDIS_PORT_URL = os.getenv('REDIS_PORT_URL')
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS")

TIME_ZONE = os.getenv("TIME_ZONE")
USE_I18N = os.getenv("USE_I18N")
USE_L10N = os.getenv("USE_L10N")
USE_TZ = os.getenv("USE_TZ")

ROOT_URLCONF = "config.urls"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
WSGI_APPLICATION = "config.wsgi.application"

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR / 'static')


INSTALLED_APPS = [
    "jazzmin",
    "modeltranslation",
    "drf_spectacular",
    "debug_toolbar",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",

]


INSTALLED_APPS += [
    'apps.authentication.apps.AuthenticationConfig',
    'apps.base.apps.BaseConfig',
    'apps.users.apps.UsersConfig',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator", },
    {"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator", },
]
