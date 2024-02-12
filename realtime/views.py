from django.shortcuts import render, HttpResponse

from .tasks import test_celery, hello_celery

# Create your views here.


def test(request):
    text = test_celery.delay()
    return HttpResponse(text.get())


def hello(request):
    hello_celery.delay(2, 3)
    return HttpResponse("Hello, world!")
