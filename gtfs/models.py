import re
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from django.db.models.signals import post_save

from alerts.multicast import test_signal


def validate_no_spaces_or_special_symbols(value):
    if re.search(r"[^a-zA-Z0-9_]", value):
        raise ValidationError(
            "Este campo no puede contener espacios ni símbolos especiales, solamente letras, números y guiones bajos."
        )


class GTFSProvider(models.Model):
    """A provider provides transportation services GTFS data.

    It might or might not be the same as the agency in the GTFS feed. A GTFS provider can serve multiple agencies.
    """

    provider_id = models.BigAutoField(primary_key=True)
    code = models.CharField(
        max_length=31,
        help_text="Código (típicamente el acrónimo) de la empresa. No debe tener espacios ni símbolos especiales.",
        validators=[validate_no_spaces_or_special_symbols],
    )
    name = models.CharField(max_length=255, help_text="Nombre de la empresa.")
    description = models.TextField(
        blank=True, null=True, help_text="Descripción de la institución o empresa."
    )
    website = models.URLField(
        blank=True, null=True, help_text="Sitio web de la empresa."
    )
    schedule_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL del suministro (Feed) de GTFS Schedule (.zip).",
    )
    trip_updates_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL del suministro (FeedMessage) de la entidad GTFS Realtime TripUpdates (.pb).",
    )
    vehicle_positions_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL del suministro (FeedMessage) de la entidad GTFS Realtime VehiclePositions (.pb).",
    )
    service_alerts_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL del suministro (FeedMessage) de la entidad GTFS Realtime ServiceAlerts (.pb).",
    )
    timezone = models.CharField(
        max_length=63,
        help_text="Zona horaria del proveedor de datos (asume misma zona horaria para todas las agencias). Ejemplo: America/Costa_Rica.",
    )
    is_active = models.BooleanField(
        default=False,
        help_text="¿Está activo el proveedor de datos? Si no, no se importarán los datos de este proveedor.",
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


# -------------
# GTFS Schedule
# -------------


class Feed(models.Model):
    feed_id = models.CharField(max_length=100, primary_key=True, unique=True)
    provider = models.ForeignKey(
        GTFSProvider, on_delete=models.SET_NULL, blank=True, null=True
    )
    http_etag = models.CharField(max_length=1023, blank=True, null=True)
    http_last_modified = models.DateTimeField(blank=True, null=True)
    is_current = models.BooleanField(blank=True, null=True)
    retrieved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.feed_id


class Agency(models.Model):
    """One or more transit agencies that provide the data in this feed.
    Maps to agency.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, to_field="feed_id", on_delete=models.CASCADE)
    agency_id = models.CharField(
        max_length=255,
        blank=True,
        help_text="Identificador único de la agencia de transportes.",
    )
    agency_name = models.CharField(
        max_length=255, help_text="Nombre completo de la agencia de transportes."
    )
    agency_url = models.URLField(help_text="URL de la agencia de transportes.")
    agency_timezone = models.CharField(
        max_length=255, help_text="Zona horaria de la agencia de transportes."
    )
    agency_lang = models.CharField(
        max_length=2, blank=True, help_text="Código ISO 639-1 de idioma primario."
    )
    agency_phone = models.CharField(
        max_length=127, blank=True, null=True, help_text="Número de teléfono."
    )
    agency_fare_url = models.URLField(
        blank=True, null=True, help_text="URL para la compra de tiquetes en línea."
    )
    agency_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        help_text="Correo electrónico de servicio al cliente.",
    )

    class Meta:
        verbose_name = "agency"
        verbose_name_plural = "agencies"

    # TODO: colocar las restricciones con unique_constraint. Por ejemplo: la combinación agency_id + feed debe ser única.

    def __str__(self):
        return self.agency_name


class Stop(models.Model):
    """Individual locations where vehicles pick up or drop off riders.
    Maps to stops.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    stop_id = models.CharField(
        max_length=255, help_text="Identificador único de la parada."
    )
    stop_code = models.CharField(
        max_length=255, blank=True, null=True, help_text="Código de la parada."
    )
    stop_name = models.CharField(max_length=255, help_text="Nombre de la parada.")
    stop_desc = models.TextField(
        blank=True, null=True, help_text="Descripción de la parada."
    )
    stop_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Latitud de la parada.",
    )
    stop_lon = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Longitud de la parada.",
    )
    stop_point = models.PointField(
        blank=True, null=True, help_text="Punto georreferenciado de la parada."
    )
    zone_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="Identificador de la zona."
    )
    stop_url = models.URLField(blank=True, null=True, help_text="URL de la parada.")
    location_type = models.PositiveIntegerField(
        blank=True, null=True, help_text="Tipo de parada."
    )
    parent_station = models.CharField(
        max_length=255, blank=True, help_text="Estación principal."
    )
    stop_timezone = models.CharField(
        max_length=255, blank=True, help_text="Zona horaria de la parada."
    )
    wheelchair_boarding = models.PositiveIntegerField(
        blank=True, null=True, help_text="Acceso para sillas de ruedas."
    )
    level_id = models.CharField(
        max_length=255, blank=True, help_text="Identificador del nivel."
    )
    platform_code = models.CharField(
        max_length=255, blank=True, help_text="Código de la plataforma."
    )

    # Build stop_point from stop_lat and stop_lon
    # def save(self, *args, **kwargs):
    #    self.stop_point = Point(self.stop_lon, self.stop_lat)
    #    super(Stop, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.stop_id}: {self.stop_name}"


class Route(models.Model):
    """A group of trips that are displayed to riders as a single service.
    Maps to routes.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    route_id = models.CharField(
        max_length=255, help_text="Identificador único de la ruta."
    )
    agency_id = models.CharField(max_length=200)
    route_short_name = models.CharField(
        max_length=63, blank=True, null=True, help_text="Nombre corto de la ruta."
    )
    route_long_name = models.CharField(
        max_length=255, help_text="Nombre largo de la ruta."
    )
    route_desc = models.TextField(
        blank=True, null=True, help_text="Descripción de la ruta."
    )
    route_type = models.PositiveIntegerField(
        choices=(
            (0, "Tranvía o tren ligero."),
            (1, "Subterráneo o metro."),
            (2, "Ferrocarril."),
            (3, "Bus."),
            (4, "Ferry."),
            (5, "Teleférico."),
            (6, "Góndola."),
            (7, "Funicular."),
        ),
        help_text="Tipo de ruta (bus, subway, train, tram, ferry, cable car, gondola, funicular).",
    )
    route_url = models.URLField(
        blank=True, null=True, help_text="URL de la ruta en el sitio web de la agencia."
    )
    route_color = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        help_text="Color que representa la ruta en formato hexadecimal.",
    )
    route_text_color = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        help_text="Color del texto que representa la ruta en formato hexadecimal.",
    )
    route_sort_order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.route_short_name}: {self.route_long_name}"


class Calendar(models.Model):
    """Dates for service IDs using a weekly schedule.
    Maps to calendar.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    service_id = models.CharField(
        max_length=255, help_text="Identificador único del servicio."
    )
    monday = models.BooleanField(help_text="Lunes")
    tuesday = models.BooleanField(help_text="Martes")
    wednesday = models.BooleanField(help_text="Miércoles")
    thursday = models.BooleanField(help_text="Jueves")
    friday = models.BooleanField(help_text="Viernes")
    saturday = models.BooleanField(help_text="Sábado")
    sunday = models.BooleanField(help_text="Domingo")
    start_date = models.DateField(help_text="Fecha de inicio del servicio.")
    end_date = models.DateField(help_text="Fecha de finalización del servicio.")

    def __str__(self):
        return self.service_id


class CalendarDate(models.Model):
    """Exceptions for the service IDs defined in the calendar.txt file.
    Maps to calendar_dates.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    service_id = models.CharField(
        max_length=255, help_text="Identificador único del servicio."
    )
    date = models.DateField(help_text="Fecha de excepción.")
    exception_type = models.PositiveIntegerField(
        choices=((1, "Agregar"), (2, "Eliminar")), help_text="Tipo de excepción."
    )
    holiday_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.holiday_name} ({self.service_id})"


class Shape(models.Model):
    """Rules for drawing lines on a map to represent a transit organization's routes.
    Maps to shapes.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    shape_id = models.CharField(
        max_length=255, help_text="Identificador único de la trayectoria."
    )
    shape_pt_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Latitud de un punto en la trayectoria.",
    )
    shape_pt_lon = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Longitud de un punto en la trayectoria.",
    )
    shape_pt_sequence = models.PositiveIntegerField(
        help_text="Secuencia del punto en la trayectoria."
    )
    shape_dist_traveled = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        blank=True,
        null=True,
        help_text="Distancia recorrida en la trayectoria.",
    )

    def __str__(self):
        return self.shape_id


class GeoShape(models.Model):
    """Rules for drawing lines on a map to represent a transit organization's routes.
    Maps to shapes.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    shape_id = models.CharField(
        max_length=255, help_text="Identificador único de la trayectoria."
    )
    geometry = models.LineStringField(
        help_text="Trayectoria de la ruta.",
        # dim=3, # To store 3D coordinates (x, y, z)
    )
    has_altitude = models.BooleanField(
        help_text="Indica si la trayectoria tiene datos de altitud", default=False
    )

    def __str__(self):
        return self.shape_id


class Trip(models.Model):
    """Trips for each route. A trip is a sequence of two or more stops that occurs at specific time.
    Maps to trips.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    route_id = models.CharField(max_length=200)
    service_id = models.CharField(max_length=200)
    trip_id = models.CharField(
        max_length=255, help_text="Identificador único del viaje."
    )
    trip_headsign = models.CharField(
        max_length=255, blank=True, null=True, help_text="Destino del viaje."
    )
    trip_short_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="Nombre corto del viaje."
    )
    direction_id = models.PositiveIntegerField(
        choices=((0, "En un sentido"), (1, "En el otro")),
        help_text="Dirección del viaje.",
    )
    block_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="Identificador del bloque."
    )
    shape_id = models.CharField(max_length=255, blank=True, null=True)
    geoshape = models.ForeignKey(
        GeoShape, on_delete=models.SET_NULL, blank=True, null=True
    )
    wheelchair_accessible = models.PositiveIntegerField(
        choices=((0, "No especificado"), (1, "Accesible"), (2, "No accesible")),
        help_text="¿Tiene acceso para sillas de ruedas?",
    )
    bikes_allowed = models.PositiveIntegerField(
        choices=((0, "No especificado"), (1, "Permitido"), (2, "No permitido")),
        help_text="¿ Es permitido llevar bicicletas?",
    )

    def __str__(self):
        return self.trip_id


class StopTime(models.Model):
    """Times that a vehicle arrives at and departs from individual stops for each trip.
    Maps to stop_times.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    trip_id = models.CharField(max_length=200)
    arrival_time = models.TimeField(
        help_text="Hora de llegada a la parada.", blank=True, null=True
    )
    departure_time = models.TimeField(
        help_text="Hora de salida de la parada.", blank=True, null=True
    )
    stop_id = models.CharField(max_length=200)
    stop_sequence = models.PositiveIntegerField(
        help_text="Secuencia de la parada en el viaje."
    )
    stop_headsign = models.CharField(
        max_length=255, blank=True, null=True, help_text="Destino de la parada."
    )
    pickup_type = models.PositiveIntegerField(
        help_text="Tipo de recogida de pasajeros.",
    )
    drop_off_type = models.PositiveIntegerField(
        help_text="Tipo de bajada de pasajeros.",
    )
    shape_dist_traveled = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        blank=True,
        null=True,
        help_text="Distancia recorrida en la trayectoria.",
    )
    timepoint = models.BooleanField(
        blank=True,
        null=True,
        help_text="¿Es un punto de tiempo programado?",
    )

    def __str__(self):
        return f"{self.trip_id}: {self.stop_id} ({self.stop_sequence})"


class FeedInfo(models.Model):
    """Additional information about the feed itself, including publisher, version, and expiration information.
    Maps to feed_info.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    feed_publisher_name = models.CharField(
        max_length=255, help_text="Nombre del editor del feed."
    )
    feed_publisher_url = models.URLField(
        help_text="URL del editor del feed.", blank=True, null=True
    )
    feed_lang = models.CharField(
        max_length=2, help_text="Código ISO 639-1 de idioma primario."
    )
    feed_start_date = models.DateField(
        help_text="Fecha de inicio de la información del feed.", blank=True, null=True
    )
    feed_end_date = models.DateField(
        help_text="Fecha de finalización de la información del feed.",
        blank=True,
        null=True,
    )
    feed_version = models.CharField(
        max_length=255, blank=True, null=True, help_text="Versión del feed."
    )

    def __str__(self):
        return f"{self.feed_publisher_name}: {self.feed_version}"


class FareAttribute(models.Model):
    """Rules for how to calculate the fare for a certain kind of trip.
    Maps to fare_attributes.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    fare_id = models.CharField(
        max_length=255, help_text="Identificador único de la tarifa."
    )
    price = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Precio de la tarifa."
    )
    currency_type = models.CharField(
        max_length=3, help_text="Código ISO 4217 de la moneda."
    )
    payment_method = models.PositiveIntegerField(
        choices=((0, "Pago a bordo"), (1, "Pago anticipado")),
        help_text="Método de pago.",
    )
    transfers = models.PositiveIntegerField(
        choices=(
            (0, "No permitido"),
            (1, "Permitido"),
            (2, "Permitido dentro de la misma agencia"),
        ),
        help_text="Número de transferencias permitidas.",
    )
    transfer_duration = models.PositiveIntegerField(
        blank=True, null=True, help_text="Duración de la transferencia."
    )

    def __str__(self):
        return self.fare_id


class FareRule(models.Model):
    """Rules for which fare to apply in a given situation.
    Maps to fare_rules.txt in the GTFS feed.
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    fare_id = models.CharField(max_length=200)
    route_id = models.CharField(max_length=200)
    origin_id = models.CharField(max_length=255, blank=True, null=True)
    destination_id = models.CharField(max_length=255, blank=True, null=True)
    contains_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.fare_id}: {self.route_id}"


# -------------
# GTFS Realtime
# -------------


class FeedMessage(models.Model):
    """
    Header of a GTFS Realtime FeedMessage.

    This is metadata to link records of other models to a retrieved FeedMessage containing several entities, typically (necessarily, in this implementation) of a single kind.
    """

    ENTITY_TYPE_CHOICES = (
        ("trip_update", "TripUpdate"),
        ("vehicle", "VehiclePosition"),
        ("alert", "Alert"),
    )

    feed_message_id = models.CharField(max_length=63, primary_key=True)
    provider = models.ForeignKey(
        GTFSProvider, on_delete=models.SET_NULL, blank=True, null=True
    )
    entity_type = models.CharField(max_length=63, choices=ENTITY_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now=True)
    incrementality = models.CharField(max_length=15)
    gtfs_realtime_version = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.entity_type} ({self.timestamp})"


class TripUpdate(models.Model):
    """
    GTFS Realtime TripUpdate entity v2.0 (normalized).

    Trip updates represent fluctuations in the timetable.
    """

    id = models.BigAutoField(primary_key=True)
    entity_id = models.CharField(max_length=127)

    # Foreign key to FeedMessage model
    feed_message = models.ForeignKey("FeedMessage", on_delete=models.CASCADE)

    # TripDescriptor (message)
    trip_trip_id = models.CharField(max_length=255, blank=True, null=True)
    trip_route_id = models.CharField(max_length=255, blank=True, null=True)
    trip_direction_id = models.IntegerField(blank=True, null=True)
    trip_start_time = models.DurationField(blank=True, null=True)
    trip_start_date = models.DateField(blank=True, null=True)
    trip_schedule_relationship = models.CharField(
        max_length=31, blank=True, null=True
    )  # (enum)

    # VehicleDescriptor (message)
    vehicle_id = models.CharField(max_length=255, blank=True, null=True)
    vehicle_label = models.CharField(max_length=255, blank=True, null=True)
    vehicle_license_plate = models.CharField(max_length=255, blank=True, null=True)
    vehicle_wheelchair_accessible = models.CharField(
        max_length=31, blank=True, null=True
    )  # (enum)

    # Timestamp (uint64)
    timestamp = models.DateTimeField(blank=True, null=True)

    # Delay (int32)
    delay = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.entity_id} ({self.feed_message})"


class StopTimeUpdate(models.Model):
    """
    GTFS Realtime TripUpdate message v2.0 (normalized).

    Realtime update for arrival and/or departure events for a given stop on a trip, linked to a TripUpdate entity in a FeedMessage.
    """

    id = models.BigAutoField(primary_key=True)

    # Foreign key to FeedMessage and TripUpdate models
    feed_message = models.ForeignKey(FeedMessage, on_delete=models.CASCADE)
    trip_update = models.ForeignKey(TripUpdate, on_delete=models.CASCADE)

    # Stop ID (string)
    stop_sequence = models.IntegerField(blank=True, null=True)
    stop_id = models.CharField(max_length=127, blank=True, null=True)

    # StopTimeEvent (message): arrival
    arrival_delay = models.IntegerField(blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    arrival_uncertainty = models.IntegerField(blank=True, null=True)

    # StopTimeEvent (message): departure
    departure_delay = models.IntegerField(blank=True, null=True)
    departure_time = models.DateTimeField(blank=True, null=True)
    departure_uncertainty = models.IntegerField(blank=True, null=True)

    # OccupancyStatus (enum)
    departure_occupancy_status = models.CharField(max_length=255, blank=True, null=True)

    # ScheduleRelationship (enum)
    schedule_relationship = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.stop_id} ({self.trip_update})"


class VehiclePosition(models.Model):
    """
    GTFS Realtime VehiclePosition entity v2.0 (normalized).

    Vehicle position represents a few basic pieces of information about a particular vehicle on the network.
    """

    id = models.BigAutoField(primary_key=True)
    entity_id = models.CharField(max_length=127)

    # Foreign key to FeedMessage model
    feed_message = models.ForeignKey(
        FeedMessage, on_delete=models.CASCADE, blank=True, null=True
    )

    # TripDescriptor (message)
    vehicle_trip_trip_id = models.CharField(max_length=255)
    vehicle_trip_route_id = models.CharField(max_length=255, blank=True, null=True)
    vehicle_trip_direction_id = models.IntegerField(blank=True, null=True)
    vehicle_trip_start_time = models.DurationField(blank=True, null=True)
    vehicle_trip_start_date = models.DateField(blank=True, null=True)
    vehicle_trip_schedule_relationship = models.CharField(
        max_length=31, blank=True, null=True
    )  # (enum)

    # VehicleDescriptor (message)
    vehicle_vehicle_id = models.CharField(max_length=255, blank=True, null=True)
    vehicle_vehicle_label = models.CharField(max_length=255, blank=True, null=True)
    vehicle_vehicle_license_plate = models.CharField(
        max_length=255, blank=True, null=True
    )
    vehicle_vehicle_wheelchair_accessible = models.CharField(
        max_length=31, blank=True, null=True
    )  # (enum)

    # Position (message)
    vehicle_position_latitude = models.FloatField(blank=True, null=True)
    vehicle_position_longitude = models.FloatField(blank=True, null=True)
    vehicle_position_point = models.PointField(srid=4326, blank=True, null=True)
    vehicle_position_bearing = models.FloatField(blank=True, null=True)
    vehicle_position_odometer = models.FloatField(blank=True, null=True)
    vehicle_position_speed = models.FloatField(blank=True, null=True)  # (meters/second)

    # Current stop sequence (uint32)
    vehicle_current_stop_sequence = models.IntegerField(blank=True, null=True)

    # Stop ID (string)
    vehicle_stop_id = models.CharField(max_length=255, blank=True, null=True)

    # VehicleStopStatus (enum)
    vehicle_current_status = models.CharField(max_length=255, blank=True, null=True)

    # Timestamp (uint64)
    vehicle_timestamp = models.DateTimeField(blank=True, null=True)

    # CongestionLevel (enum)
    vehicle_congestion_level = models.CharField(max_length=255, blank=True, null=True)

    # OccupancyStatus (enum)
    vehicle_occupancy_status = models.CharField(max_length=255, blank=True, null=True)

    # OccupancyPercentage (uint32)
    vehicle_occupancy_percentage = models.FloatField(blank=True, null=True)

    # CarriageDetails (message): not implemented

    def save(self, *args, **kwargs):
        self.vehicle_position_point = Point(
            self.vehicle_position_longitude, self.vehicle_position_latitude
        )
        super(VehiclePosition, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.entity_id} ({self.feed_message})"


class Alert(models.Model):
    """Alerts and warnings about the service.
    Maps to alerts.txt in the GTFS feed.

    TODO: ajustar con Alerts de GTFS Realtime
    """

    id = models.BigAutoField(primary_key=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    alert_id = models.CharField(
        max_length=255, help_text="Identificador único de la alerta."
    )
    route_id = models.CharField(max_length=255, help_text="Identificador de la ruta.")
    trip_id = models.CharField(max_length=255, help_text="Identificador del viaje.")
    service_date = models.DateField(
        help_text="Fecha del servicio descrito por la alerta."
    )
    service_start_time = models.TimeField(
        help_text="Hora de inicio del servicio descrito por la alerta."
    )
    service_end_time = models.TimeField(
        help_text="Hora de finalización del servicio descrito por la alerta."
    )
    alert_header = models.CharField(
        max_length=255, help_text="Encabezado de la alerta."
    )
    alert_description = models.TextField(help_text="Descripción de la alerta.")
    alert_url = models.URLField(blank=True, null=True, help_text="URL de la alerta.")
    cause = models.PositiveIntegerField(
        choices=(
            (1, "Otra causa"),
            (2, "Accidente"),
            (3, "Congestión"),
            (4, "Evento"),
            (5, "Mantenimiento"),
            (6, "Planificado"),
            (7, "Huelga"),
            (8, "Manifestación"),
            (9, "Demora"),
            (10, "Cierre"),
        ),
        help_text="Causa de la alerta.",
    )
    effect = models.PositiveIntegerField(
        choices=(
            (1, "Otro efecto"),
            (2, "Desviación"),
            (3, "Adelanto"),
            (4, "Cancelación"),
            (5, "Cierre"),
            (6, "Desvío"),
            (7, "Detención"),
            (8, "Desconocido"),
        ),
        help_text="Efecto de la alerta.",
    )
    severity = models.PositiveIntegerField(
        choices=(
            (1, "Desconocido"),
            (2, "Información"),
            (3, "Advertencia"),
            (4, "Grave"),
            (5, "Muy grave"),
        ),
        help_text="Severidad de la alerta.",
    )
    published = models.DateTimeField(
        help_text="Fecha y hora de publicación de la alerta."
    )
    updated = models.DateTimeField(
        help_text="Fecha y hora de actualización de la alerta."
    )
    informed_entity = models.JSONField(help_text="Entidades informadas por la alerta.")

    def __str__(self):
        return self.alert_id


# -------
# Records
# -------


class Record(models.Model):
    """A log of the GTFS Schedule updating sessions."""

    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)
    provider = models.ForeignKey(
        GTFSProvider, on_delete=models.SET_NULL, blank=True, null=True
    )
    data_source = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.feed_transit_system} ({self.timestamp})"


# Django Model Signal (find a good place for this)
post_save.connect(test_signal, sender=Record)
