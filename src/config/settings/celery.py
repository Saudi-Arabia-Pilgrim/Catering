import os

from celery.schedules import crontab
from dotenv import load_dotenv


load_dotenv()

CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_TASK_SERIALIZER = os.getenv('CELERY_TASK_SERIALIZER')
CELERY_RESULT_SERIALIZER = os.getenv('CELERY_RESULT_SERIALIZER')
CELERY_TASK_TRACK_STARTED = os.getenv('CELERY_TASK_TRACK_STARTED')
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = os.getenv('CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP')



CELERY_BEAT_SCHEDULE = {
    'update-daily-guest-prices-every-midnight': {
        'task': 'apps.guests.tasks.update_daily_guest_prices',
        'schedule': crontab(minute=0, hour=0),  # Run every 1 minute
    },
}