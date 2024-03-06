from django.shortcuts import render

# Create your views here.


def realtime(request):
    return render(request, "realtime.html")
