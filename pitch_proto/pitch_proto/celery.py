import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pitch_proto.settings')

app = Celery('pitch_proto')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'get_joke_4s': {
        'task': 'jokes.tasks.get_joke',
        'schedule': 4.0
    }
}

app.autodiscover_tasks()
