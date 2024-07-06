from django.conf import settings
from django.http import FileResponse
from feed.models import InfoService
from gtfs.models import GTFSProvider, Route, Trip
from rest_framework import viewsets, permissions

from .serializers import InfoServiceSerializer, GTFSProviderSerializer, RouteSerializer, TripSerializer


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


class TripViewSet(viewsets.ModelViewSet):
    """
    Viajes de transporte público.
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        # Initial queryset before (possible) filtering
        queryset = Trip.objects.all()
        # Get query parameters
        trip_id = self.request.query_params.get("trip_id")
        route_id = self.request.query_params.get("route_id")
        # Filter queryset if needed, based on query parameters
        if trip_id is not None:
            queryset = queryset.filter(trip_id=trip_id)
        elif route_id is not None:
            queryset = queryset.filter(route_id=route_id)
        return queryset

    # permission_classes = [permissions.IsAuthenticated]


def get_schema(request):
    file_path = settings.BASE_DIR / "api" / "datahub.yml"
    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="datahub.yml"
    )
