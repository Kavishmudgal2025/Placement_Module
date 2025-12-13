from celery import shared_task
from datetime import date
from .models import Job

@shared_task
def deactivate_expired_jobs():
    expired_jobs = Job.objects.filter(active_status=True, application_deadline__lt=date.today())
    expired_jobs.update(active_status=False) 
    return f"{expired_jobs.count()} jobs deactivated."
