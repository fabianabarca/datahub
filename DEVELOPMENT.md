# Desarrollo funcional

En esencia, el servidor hace:

- Desplegar información en pantallas por medio de un navegador web (Chromium) y actualizar los datos con WebSockets utilizando [Django Channels](https://channels.readthedocs.io/en/latest/).
- Tareas periódicas de revisión de información actualizada, utilizando [Celery](https://docs.celeryq.dev/en/stable/index.html) como manejador de tareas (_task manager_).
- Panel de administración para agregar/quitar pantallas, configurar parámetros, etc.

Aplicaciones:

- `gtfs`: recopila los datos de GTFS Schedule y GTFS Realtime.
- `screens`: realiza las tareas periódicas de actualización.
- `website`: administra el panel de administración.

## Recopilación de `FeedMessage` cada $N$ segundos
  - Opciones: Apache Airflow o como proceso del sistema con paquetes de Python para tareas repetitivas (versión más fácil).
  - Es necesario usar los paquetes de Google para procesar los `.pb` y convertirlo a un diccionario o un JSON o un DataFrame de Pandas.

## *Script* de clasificación y ordenamiento de GTFS Realtime

Es necesario separar los datos que son relevantes para cada parada (¿tópicos?).

- Es posible trabajarlo con puro Python (sin preocuparse todavía de Django)
- Aquí es importante la eficiencia computacional (un poco)
- Herramientas posibles: ¿Pandas? (muy lento), o guardar directamente a la base de datos y ordernarlo desde ahí.
- Depende del análisis del GTFS del sistema de buses, porque hay que analizar cuáles buses van a pasar o ya pasaron por una parada en particular, etc.
- También hay que definir el formato de lo datos que serán compartidos (ya no es GTFS Realtime, necesariamente).

## Actualización de la información de cada pantalla 

(Django WebSockets)

## Configuración del hardware de las pantallas 

(Raspberry Pi)

Ejemplo de primer prototipo: Soda de Ingeniería (no requiere protección).
