from django.conf import settings
from django.http import FileResponse
from feed.models import Application
from gtfs.models import Provider
from rest_framework import viewsets, permissions

from .serializers import ApplicationSerializer, ProviderSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Aplicaciones conectadas al servidor de datos.
    """

    queryset = Application.objects.all().order_by("created_at")
    serializer_class = ApplicationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ProviderViewSet(viewsets.ModelViewSet):
    """
    Proveedores de datos GTFS.
    """

    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    # permission_classes = [permissions.IsAuthenticated]


def get_schema(request):
    file_path = settings.BASE_DIR / "api" / "datahub.yml"
    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="datahub.yml"
    )
