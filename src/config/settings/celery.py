import os

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
    # 'example-task': {
    #     'task': 'apps.base.tasks.example_task.example_task',
    #     'schedule': crontab(hour="1"),  # Run every 1 minute
    # },
}