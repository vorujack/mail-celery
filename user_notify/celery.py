import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_notify.settings')

app = Celery('user_notify')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
