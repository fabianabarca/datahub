from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from . import views

router = routers.DefaultRouter()
router.register(r"info-services", views.InfoServiceViewSet)
router.register(r"gtfs-providers", views.GTFSProviderViewSet)
router.register(r"routes", views.RouteViewSet)
router.register(r"trips", views.TripViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("docs/schema/", views.get_schema, name="schema"),
    path("docs/", SpectacularRedocView.as_view(url_name="schema"), name="api_docs"),
]
