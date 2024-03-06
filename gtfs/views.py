from django.shortcuts import render

# Create your views here.


def gtfs(request):
    return render(request, "gtfs.html")


def schedule(request):
    return render(request, "schedule.html")


def realtime(request):
    return render(request, "realtime.html")


def company(request):
    return render(request, "company.html")