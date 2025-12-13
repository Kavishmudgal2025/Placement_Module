"""from models import Job
from datetime import date

def active_status():
    status = Job.objects.filter(active_status=True, application_deadline__lt=date.today())
    if active_status == True:
        status.update(active_status=False)
        return status
    return status"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement.settings')

app = Celery('placement')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


