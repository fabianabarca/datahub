from django.urls import path

from . import views

urlpatterns = [
    path("", views.gtfs),
    path("schedule/", views.schedule, name="schedule"),
    path("realtime/", views.realtime, name="realtime"),
    path("compania/", views.company, name="company"),
]