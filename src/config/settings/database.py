import os

from django.conf import settings

POSTGRES = True

if POSTGRES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['POSTGRES_DB'],
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
            'HOST': os.environ['DB_HOST'],
            'PORT': os.environ['DB_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': settings.BASE_DIR / 'db.sqlite3',
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'{settings.REDIS_PORT_URL}/2',
    }
}
