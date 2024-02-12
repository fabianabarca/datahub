# Create your tasks here

from .models import Test

from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import requests
from time import sleep


@shared_task
def test_celery():
    response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    text = response.json()["text"]
    Test.objects.create(text=text)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "screen",
        {
            "type": "screen_message",
            "message": text,
        },
    )
    return text


@shared_task
def hello_celery(x, y):
    for i in range(6):
        print(i)
        sleep(1)
    return f"Done! {x} + {y} = {x + y}"


@shared_task
def get_vehiclepositions():
    return "VehiclePositions"


@shared_task
def get_tripupdates():
    return "TripUpdates"


@shared_task
def get_gtfs():
    return "GTFS"