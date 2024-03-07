from celery import shared_task

import logging
import configparser
import datetime
from sqlalchemy import create_engine
import pandas as pd
import requests
from asgiref.sync import async_to_sync, sync_to_async

from .models import *


@shared_task
def get_schedule():
   
    # Logging configuration
    logging.basicConfig(
        filename="schedule.log",
        format="%(levelname)s: %(message)s",
        encoding="utf-8",
        level=logging.INFO,
    )

    # Configuration file
    # config = configparser.ConfigParser()
    # config.read("./gtfs.cfg")

    # Database information (get from .env file? It'd be better)
    system = "postgresql" # config.get("database", "system")
    host = "localhost" # config.get("database", "host")
    port = 5432 # config.get("database", "port")
    name = "gtfs2screens" # config.get("database", "name")
    user = "fabian" # config.get("database", "user")
    password = "" # config.get("database", "password")

    # Create database engine
    engine = create_engine(f"{system}://{user}:{password}@{host}:{port}/{name}")

    # GTFS information
    feed_transit_system = "MBTA" # config.get("gtfs", "transit_system")
    schedule_url = "https://cdn.mbta.com/MBTA_GTFS.zip" # config.get("gtfs", "schedule_url")
    tables = {
        "agency": "Agency",
        "stops": "Stop",
        "shapes": "Shape",
        "calendar": "Calendar",
        "calendar_dates": "CalendarDate",
        "routes": "Route",
        "trips": "Trip",
        "stop_times": "StopTime",
        "frequencies": "Frequency",
        "feed_info": "FeedInfo",
    }  # They must be loaded in this order

    logging.info(
        f"New GTFS Schedule updating session\n{feed_transit_system}\n{datetime.datetime.now()}\nData source: {schedule_url}"
    )

    # Check if the feed has been updated
    last_feed_tag = {"value": None}
    try:
        last_feed_tag["value"] = (
            Feed.objects.all()
            .order_by("-retrieved_at")
            .first()
            .http_etag
        )
    except:
        logging.info("No http_etag found in the table 'feeds'!")
        logging.info("A new feed will be imported!")

    logging.info(f"Performing fetch at {datetime.datetime.now()}")

    schedule_check = requests.head(schedule_url)
    feed_tag = schedule_check.headers["ETag"]

    if not feed_tag == last_feed_tag["value"]:
        logging.info(f"New GTFS Schedule feed detected: {feed_tag}")
        logging.info("Importing new feed")

        # Save new Feed record
        last_modified = datetime.datetime.strptime(
            schedule_check.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z"
        )
        feed_id = last_modified.strftime("%Y-%m-%dT%H:%M:%S")
        # Save to database with the Feed model
        Feed.objects.create(
            feed_id=feed_id,
            http_etag=feed_tag,
            last_modified=last_modified,
        )

    return "Fetching Schedule"


@shared_task
def get_vehiclepositions():
    return "Fetching VehiclePositions"


@shared_task
def get_tripupdates():
    return "Fetching TripUpdates"
