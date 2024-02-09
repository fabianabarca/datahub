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

```bash
sudo apt install postgresql
(...)
sudo apt install postgis
```

Modificar `pg_hba.conf` de forma que sea:

```text
local    all    postgres   trust

local    all    all        trust
```
y así no tendrá contraseñas. Luego en la terminal:

```bash
sudo -u postgres psql
```

que nos lleva a la interfaz de `psql` para configurar un nuevo usuario:

```bash
postgres=# CREATE ROLE user_name SUPERUSER;
postgres=# ALTER ROLE user_name LOGIN;
```

Ahora podemos crear una base de datos, para este proyecto:

```bash
createdb gtfs2screens
```

ahora hay que ingresar a esa base de datos:

```bash
psql gtfs2screens
```

y ahí crear la extensión de PostGIS con:

```bash
gtfs2screens=# CREATE EXTENSION postgis;
```

Con esto quedaría lista la base de datos para conectarnos desde Django.

## Celery

Celery es un administrador de tareas (_task manager_)...

### Celery

Instalar Celery...

```bash
pip install version
```

y probar con `celery --version`.

Ejecutar Celery con:

```bash
celery -A gtfs2screens worker --loglevel=info
```

### Celery Beat

Celery utiliza los paquetes de integración con Django `django-celery-results` y `django-celery-beat`, y el intermediador de mensajes Redis.

```bash
celery -A gtfs2screens beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info
```

## Redis

```bash
sudo apt install redis-server
```

Nota: en macOS:

```bash
brew install redis
```

Probar su estado como proceso del sistema:

```bash
sudo systemctl status redis-server
```

Probar la conexión:

```bash
>>> redis-cli ping
PONG
```