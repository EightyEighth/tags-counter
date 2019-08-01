from __future__ import absolute_import, unicode_literals
import os
from decouple import config
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        os.environ.get('DJANGO_SETTINGS_MODULE',
                       config('DJANGO_SETTINGS_MODULE', cast=str)))
os.environ.setdefault(
        'DJANGO_CONFIGURATION',
        os.environ.get('DJANGO_CONFIGURATION',
                       config('DJANGO_CONFIGURATION', cast=str)))

app = Celery('tagcounter')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
import configurations
configurations.setup()

@app.task(name='celery.ping')
def ping():
    # type: () -> str
    """Simple task that just returns 'pong'."""
    return 'pong'
