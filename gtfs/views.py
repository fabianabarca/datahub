from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.


def gtfs(request):
    return render(request, "gtfs.html")


def schedule(request):
    users = User.objects.all()
    print(users)
    context = {
        "users": users,
    }
    return render(request, "schedule.html", context)


def realtime(request):
    return render(request, "realtime.html")


def company(request):
    return render(request, "company.html")