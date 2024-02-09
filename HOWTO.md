# Instrucciones de ejecución de la plataforma

El sistema requiere de:

- Django / Python
- PostgreSQL / PostGIS
- Celery / Celery Beat
- Redis

## Django

La plataforma de Django será útil para:

- Crear el sitio web con el panel de administración
- Administrar las tareas periódicas con su integración con Celery y Celery Beat
- Actualizar la informació en tiempo real con las pantallas con WebSockets

Es necesario instalar Django 5.0 y la extensión Django Channels:

```bash
pip install django
pip install channels
```

## PostgreSQL / PostGIS

El proyecto requiere de una base de datos con una extensión para datos geoespaciales...

## Celery

Celery es un administrador de tareas (_task manager_)...

### Celery

Instalar Celery...

Ejecutar Celery con:

```bash
celery -A gtfs2screens worker
```

### Celery Beat

Celery utiliza los paquetes de integración con Django `django-celery-results` y `django-celery-beat`, y el intermediador de mensajes Redis.

```bash
celery -A gtfs2screens beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info
```

## Redis

