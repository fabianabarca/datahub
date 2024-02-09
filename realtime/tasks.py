# Create your tasks here

from .models import Test

from celery import shared_task

import requests
from time import sleep


@shared_task
def test_celery():
    response = requests.get("https://api.chucknorris.io/jokes/random")
    joke = response.json()["value"]
    Test.objects.create(joke=joke)
    return joke


@shared_task
def hello_celery(x, y):
    for i in range(6):
        print(i)
        sleep(1)
    return f"Done! {x} + {y} = {x + y}"
