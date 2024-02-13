from django.shortcuts import render
import random

# Create your views here.


def screens(request):
    """Render a list of screens.
    """
    return render(request, "screens.html")


def create_screen(request):
    """Create and configure a new screen.
    """
    return render(request, "create_screen.html")


def screen(request, screen_id):
    """Render a screen.
    """
    seed = screen_id
    random.seed(seed)
    minutes = random.randint(0, 30)
    context = {"screen_id": screen_id, "minutes": minutes}
    return render(request, "screen.html", context)


def edit_screen(request, screen_id):
    """Edit a screen.
    """
    context = {"screen_id": screen_id}
    return render(request, "edit_screen.html", context)


def update_screen(request, screen_id):
    """Update a screen.
    """
    # Get a Django Signal signaling that the FeedMessage has been processed and there are updates for each stop.
    # For each screen, collect all data linked to it and send it, with a given format, to the screen via websocket.
    return 0


# Testing the websocket
def chat(request, room_name):
    return render(request, "chat.html", {"room_name": room_name})
