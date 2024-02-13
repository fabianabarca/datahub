from django.contrib.gis.db import models
from gtfs.models import Stop

# Create your models here.


class Screen(models.Model):
    ORIENTATION_CHOICES = [
        ("landscape", "Landscape"),
        ("portrait", "Portrait"),
    ]
    RATIO_CHOICES = [
        ("4:3", "4:3"),
        ("16:9", "16:9"),
        ("16:10", "16:10"),
    ]

    screen_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.PointField()
    address = models.TextField()
    orientation = models.CharField(
        max_length=10, choices=ORIENTATION_CHOICES, default="landscape"
    )
    ratio = models.CharField(max_length=10, choices=RATIO_CHOICES, default="16:9")
    size = models.PositiveIntegerField(help_text="in inches")
    has_audio = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ScreenStops(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.screen} - {self.stop}"
