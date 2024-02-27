# Create your tasks here

from .models import Test
from screens.models import Screen

from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async

import requests
from time import sleep


@shared_task
def test_celery():
    response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    text = response.json()["text"]
    Test.objects.create(text=text)
    channel_layer = get_channel_layer()
    screens = Screen.objects.filter(is_active=True)
    sync_to_async(print)(f"Task: {screen}")
    for screen in screens:
        async_to_sync(channel_layer.group_send)(
            f"screen_{screen.screen_id}",
            {
                "type": "screen_message",
                "message": f"{screen.screen_id}: {text}",
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