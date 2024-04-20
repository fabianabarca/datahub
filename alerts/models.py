from django.contrib.gis.db import models
from gtfs.models import Stop

# Create your models here.


class Screen(models.Model):
    ORIENTATION_CHOICES = [
        ("landscape", "Horizontal"),
        ("portrait", "Vertical"),
    ]
    RATIO_CHOICES = [
        ("4:3", "4:3"),
        ("16:9", "16:9"),
        ("16:10", "16:10"),
    ]

    screen_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.PointField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    orientation = models.CharField(
        max_length=10,
        choices=ORIENTATION_CHOICES,
        default="landscape",
        blank=True, null=True,
    )
    ratio = models.CharField(
        max_length=10, 
        choices=RATIO_CHOICES, 
        default="16:9", 
        blank=True, null=True
    )
    size = models.PositiveIntegerField(help_text="diagonal en pulgadas", blank=True, null=True)
    has_audio = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ScreenStops(models.Model):
    id = models.AutoField(primary_key=True)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.screen} - {self.stop}"
