from django.shortcuts import render

# Create your views here.


def screens(request):
    return render(request, "screens.html")


def create_screen(request):
    return render(request, "create_screen.html")


def screen(request, screen_id):
    context = {"screen_id": screen_id}
    return render(request, "screen.html", context)


def edit_screen(request, screen_id):
    context = {"screen_id": screen_id}
    return render(request, "edit_screen.html", context)
