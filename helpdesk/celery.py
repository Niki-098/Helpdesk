import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')

app = Celery('helpdesk')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# schedule periodic task to check escalations every 1 minute (for demo)
app.conf.beat_schedule = {
    'check-escalations-every-minute': {
        'task': 'tickets.tasks.check_ticket_escalations',
        'schedule': 60.0,
    },
}
