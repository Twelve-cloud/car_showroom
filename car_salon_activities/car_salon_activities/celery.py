"""
celery.py: File, containing celery app for an car_salon_activities project.
"""


import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_salon_activities.settings')

app: type[Celery] = Celery('car_salon_activities')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
