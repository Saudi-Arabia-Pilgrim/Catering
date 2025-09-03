import os
from celery import Celery

# ======== Set the default Django settings module for the Celery program ========
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ======== Create a Celery application instance ========
app = Celery('config')

# ======== Load configuration settings from Django ========
app.config_from_object('django.conf:settings', namespace='CELERY')

# ======== Automatically discover tasks in installed Django apps ========
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    # ======== Debug task to verify Celery is working ========
    print(f'Request: {self.request!r}')
