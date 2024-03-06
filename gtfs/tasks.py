from celery import shared_task


@shared_task
def get_schedule():
    return "Fetching Schedule"


@shared_task
def get_vehiclepositions():
    return "Fetching VehiclePositions"


@shared_task
def get_tripupdates():
    return "Fetching TripUpdates"
