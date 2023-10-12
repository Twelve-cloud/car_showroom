"""
celery.py: File, containing celery app for an car_salon_activities project.
"""


import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app: type[Celery] = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
