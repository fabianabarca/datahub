# Instrucciones de ejecución de la plataforma

## Celery

Celery utiliza los paquetes de integración con Django `django-celery-results` y `django-celery-beat`, y el intermediador de mensajes Redis.

```bash
celery -A gtfs2screens beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```