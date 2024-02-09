from django.urls import path

from . import views

urlpatterns = [
    path("test/", views.test, name="test"),
    path("hello/", views.hello, name="hello"),
]