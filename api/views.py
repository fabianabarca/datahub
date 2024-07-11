from django.conf import settings
from django.http import FileResponse
from feed.models import InfoService
from gtfs.models import GTFSProvider, Route, Trip
from rest_framework import viewsets, permissions

from .serializers import InfoServiceSerializer, GTFSProviderSerializer, RouteSerializer, TripSerializer

class FilterMixin:
    def get_filtered_queryset(self, allowed_query_params):
        queryset = self.queryset
        query_params = self.request.query_params
        filter_args = {param: value for param, value in query_params.items() if param in allowed_query_params and value is not None}
        return queryset.filter(**filter_args)


class InfoServiceViewSet(viewsets.ModelViewSet):
    """
    Aplicaciones conectadas al servidor de datos.
    """

    queryset = InfoService.objects.all().order_by("created_at")
    serializer_class = InfoServiceSerializer
    # permission_classes = [permissions.IsAuthenticated]


class GTFSProviderViewSet(viewsets.ModelViewSet):
    """
    Proveedores de datos GTFS.
    """

    queryset = GTFSProvider.objects.all()
    serializer_class = GTFSProviderSerializer
    # permission_classes = [permissions.IsAuthenticated]


class RouteViewSet(viewsets.ModelViewSet):
    """
    Rutas de transporte público.
    """

    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        queryset = Route.objects.all()
        route_id = self.request.query_params.get("route_id")
        if route_id is not None:
            queryset = queryset.filter(route_id=route_id)
        return queryset

    # permission_classes = [permissions.IsAuthenticated]


class TripViewSet(FilterMixin, viewsets.ModelViewSet):
    """
    Viajes de transporte público.
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    allowed_query_parameters =  ['shape_id', 'direction_id', 'trip_id', 'route_id', 'service_id']

    def get_queryset(self):
        return self.get_filtered_queryset(self.allowed_query_parameters)

    # permission_classes = [permissions.IsAuthenticated]


def get_schema(request):
    file_path = settings.BASE_DIR / "api" / "datahub.yml"
    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="datahub.yml"
    )
