import os

from celery import Celery
from prometheus_client import start_http_server

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datahub.settings")

app = Celery("datahub")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Start a Prometheus metrics server on port 8001
# start_http_server(8001)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Celery request: {self.request!r}")
