from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

from django.core.mail import EmailMultiAlternatives, send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'callservices.settings')
app = Celery('callservices')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task()
def debug_task():
    print("hola a todos")


