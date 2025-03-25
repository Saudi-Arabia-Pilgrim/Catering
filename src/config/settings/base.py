import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()



BASE_DIR = Path(__file__).resolve().parent.parent.parent

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
    "debug_toolbar",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_yasg"

]


INSTALLED_APPS += [
    'apps.authentication.apps.AuthenticationConfig',
    'apps.base.apps.BaseConfig',
    'apps.users.apps.UsersConfig',
    'apps.counter_agents.apps.CounterAgentsConfig',
    'apps.expenses.apps.ExpensesConfig',
    'apps.foods.apps.FoodsConfig',
    'apps.guests.apps.GuestsConfig',
    'apps.hotels.apps.HotelsConfig',
    'apps.menus.apps.MenusConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.products.apps.ProductsConfig',
    'apps.rooms.apps.RoomsConfig',
    'apps.sections.apps.SectionsConfig',
    'apps.transports.apps.TransportsConfig',
    'apps.warehouses.apps.WarehousesConfig',
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

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
}
