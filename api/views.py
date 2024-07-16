from django.conf import settings
from django.http import FileResponse
from feed.models import InfoService
from gtfs.models import GTFSProvider, Route, Trip
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *

# from .serializers import InfoServiceSerializer, GTFSProviderSerializer, RouteSerializer, TripSerializer


class FilterMixin:
    def get_filtered_queryset(self, allowed_query_params):
        queryset = self.queryset
        query_params = self.request.query_params
        filter_args = {
            param: value
            for param, value in query_params.items()
            if param in allowed_query_params and value is not None
        }
        return queryset.filter(**filter_args)


class GTFSProviderViewSet(viewsets.ModelViewSet):
    """
    Proveedores de datos GTFS.
    """

    queryset = GTFSProvider.objects.all()
    serializer_class = GTFSProviderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["code", "name"]
    # permission_classes = [permissions.IsAuthenticated]


class AgencyViewSet(viewsets.ModelViewSet):
    """
    Agencias de transporte público.
    """

    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["agency_id", "agency_name"]
    # permission_classes = [permissions.IsAuthenticated]


class StopViewSet(viewsets.ModelViewSet):
    """
    Paradas de transporte público.
    """

    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "route_id",
        "location_type",
        "wheelchair_boarding",
        "located_within",
        "close_to",
        "distance",
    ]
    # permission_classes = [permissions.IsAuthenticated]


class RouteViewSet(viewsets.ModelViewSet):
    """
    Rutas de transporte público.
    """

    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["route_type", "route_id"]

    # def get_queryset(self):
    #    queryset = Route.objects.all()
    #    route_id = self.request.query_params.get("route_id")
    #    if route_id is not None:
    #        queryset = queryset.filter(route_id=route_id)
    #    return queryset

    # permission_classes = [permissions.IsAuthenticated]


class CalendarViewSet(viewsets.ModelViewSet):
    """
    Calendarios de transporte público.
    """

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["service_id"]
    # permission_classes = [permissions.IsAuthenticated]


class CalendarDateViewSet(viewsets.ModelViewSet):
    """
    Fechas de calendario de transporte público.
    """

    queryset = CalendarDate.objects.all()
    serializer_class = CalendarDateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["service_id"]
    # permission_classes = [permissions.IsAuthenticated]


class ShapeViewSet(viewsets.ModelViewSet):
    """
    Formas de transporte público.
    """

    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["shape_id"]
    # permission_classes = [permissions.IsAuthenticated]


class GeoShapeViewSet(viewsets.ModelViewSet):
    """
    Formas geográficas de transporte público.
    """

    queryset = GeoShape.objects.all()
    serializer_class = GeoShapeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["shape_id"]
    # permission_classes = [permissions.IsAuthenticated]


class TripViewSet(viewsets.ModelViewSet):
    """
    Viajes de transporte público.
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["shape_id", "direction_id", "trip_id", "route_id", "service_id"]

    # allowed_query_parameters =  ['shape_id', 'direction_id', 'trip_id', 'route_id', 'service_id']

    # def get_queryset(self):
    #    return self.get_filtered_queryset(self.allowed_query_parameters)

    # permission_classes = [permissions.IsAuthenticated]


class StopTimeViewSet(viewsets.ModelViewSet):
    """
    Horarios de paradas de transporte público.
    """

    queryset = StopTime.objects.all()
    serializer_class = StopTimeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["trip_id", "stop_id"]
    # permission_classes = [permissions.IsAuthenticated]


class FeedInfoViewSet(viewsets.ModelViewSet):
    """
    Información de alimentación de transporte público.
    """

    queryset = FeedInfo.objects.all()
    serializer_class = FeedInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["feed_publisher_name"]
    # permission_classes = [permissions.IsAuthenticated]


class FareAttributeViewSet(viewsets.ModelViewSet):
    """
    Atributos de tarifa de transporte público.
    """

    queryset = FareAttribute.objects.all()
    serializer_class = FareAttributeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["shape_id", "direction_id", "trip_id", "route_id", "service_id"]
    # permission_classes = [permissions.IsAuthenticated]
    # Esto no tiene path con query params ni response schema


class FareRuleViewSet(viewsets.ModelViewSet):
    """
    Reglas de tarifa de transporte público.
    """

    queryset = FareRule.objects.all()
    serializer_class = FareRuleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["shape_id", "direction_id", "trip_id", "route_id", "service_id"]
    # permission_classes = [permissions.IsAuthenticated]
    # Esto no tiene path con query params ni response schema


class ServiceAlertViewSet(viewsets.ModelViewSet):
    """
    Alertas de servicio de transporte público.
    """

    queryset = Alert.objects.all()
    serializer_class = ServiceAlertSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "alert_id",
        "route_id",
        "trip_id",
        "service_start_time",
        "service_date",
    ]
    # permission_classes = [permissions.IsAuthenticated]


class WeatherViewSet(viewsets.ModelViewSet):
    """
    Condiciones climáticas.
    """

    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["weather_location", "weather_condition"]
    # permission_classes = [permissions.IsAuthenticated]


class SocialViewSet(viewsets.ModelViewSet):
    """
    Publicaciones en redes sociales.
    """

    queryset = Social.objects.all()
    serializer_class = SocialSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["social_media", "social_content", "social_location"]
    # permission_classes = [permissions.IsAuthenticated]


class FeedMessageViewSet(viewsets.ModelViewSet):
    """
    Mensajes de alimentación.
    """

    queryset = FeedMessage.objects.all()
    serializer_class = FeedMessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["shape_id", "direction_id", "trip_id", "route_id", "service_id"]
    # permission_classes = [permissions.IsAuthenticated]
    # Esto no tiene path con query params ni response schema


class TripUpdateViewSet(viewsets.ModelViewSet):
    """
    Actualizaciones de viaje.
    """

    queryset = TripUpdate.objects.all()
    serializer_class = TripUpdateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "trip_trip_id",
        "trip_route_id",
        "trip_start_time",
        "vehicle_id",
    ]
    # permission_classes = [permissions.IsAuthenticated]


class StopTimeUpdateViewSet(viewsets.ModelViewSet):
    """
    Actualizaciones de horario de parada.
    """

    queryset = StopTimeUpdate.objects.all()
    serializer_class = StopTimeUpdateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["shape_id", "direction_id", "trip_id", "route_id", "service_id"]

    # permission_classes = [permissions.IsAuthenticated]
    # Esto no tiene path con query params ni response schema


class VehiclePositionViewSet(viewsets.ModelViewSet):
    """
    Posiciones de vehículos.
    """

    queryset = VehiclePosition.objects.all()
    serializer_class = VehiclePositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "vehicle_vehicle_id",
        "vehicle_trip_route_id",
        "vehicle_trip_trip_id",
        "vehicle_trip_schedule_relationship",
    ]

    # permission_classes = [permissions.IsAuthenticated]


class RecordViewSet(viewsets.ModelViewSet):
    """
    Registros de datos.
    """

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["shape_id", "direction_id", "trip_id", "route_id", "service_id"]

    # permission_classes = [permissions.IsAuthenticated]
    # Esto no tiene path con query params ni response schema


class InfoServiceViewSet(viewsets.ModelViewSet):
    """
    Aplicaciones conectadas al servidor de datos.
    """

    queryset = InfoService.objects.all().order_by("created_at")
    serializer_class = InfoServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["type", "name"]
    # permission_classes = [permissions.IsAuthenticated]


def get_schema(request):
    file_path = settings.BASE_DIR / "api" / "datahub.yml"
    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="datahub.yml"
    )
