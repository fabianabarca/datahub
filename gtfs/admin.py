from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Feed)
admin.site.register(Agency)
admin.site.register(Stop)
admin.site.register(Route)
admin.site.register(Calendar)
admin.site.register(CalendarDate)
admin.site.register(Shape)
admin.site.register(GeoShape)
admin.site.register(Trip)
admin.site.register(StopTime)
admin.site.register(FeedInfo)
admin.site.register(FareAttribute)
admin.site.register(FareRule)
admin.site.register(FeedMessage)
admin.site.register(TripUpdate)
admin.site.register(StopTimeUpdate)
admin.site.register(VehiclePosition)
