from django.contrib.gis import admin
from .models import Screen, ScreenStops

# Register your models here.

admin.site.register(Screen, admin.GISModelAdmin)
admin.site.register(ScreenStops)
