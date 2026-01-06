
from django.utils import timezone
from .models import Job

def deactivate_expired_jobs():
    today = timezone.now().date()

    active_status = Job.objects.filter(application_deadline__lt = today, active_status=True)

    active_status.update(active_status=False)
