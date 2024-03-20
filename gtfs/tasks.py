from celery import shared_task

import logging
from datetime import datetime
import pytz
import zipfile
import io
import pandas as pd
import requests
from asgiref.sync import async_to_sync, sync_to_async

from .models import *


@shared_task
def get_schedule():

    # Logging configuration
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        encoding="utf-8",
        level=logging.INFO,
    )

    # GTFS information
    company = "MBTA"
    schedule_url = "https://cdn.mbta.com/MBTA_GTFS.zip"

    logging.info(
        f"GTFS Schedule updating session\n{company}\n{datetime.now()}\nData source: {schedule_url}"
    )

    # Check if the feed has been updated
    last_feed_tag = {"value": None}
    try:
        last_feed_tag["value"] = (
            Feed.objects.all().order_by("-retrieved_at").first().http_etag
        )
    except:
        logging.info("No records found in the table 'feeds'.")

    # Get the feed's ETag to compare with the last one
    schedule_check = requests.head(schedule_url)
    feed_tag = schedule_check.headers["ETag"]

    if not feed_tag == last_feed_tag["value"]:
        logging.info(f"Importing new GTFS Schedule feed detected: {feed_tag}")

        # Request feed
        schedule_response = requests.get(schedule_url)
        schedule_zip = zipfile.ZipFile(io.BytesIO(schedule_response.content))

        last_modified = schedule_check.headers["Last-Modified"]
        last_modified = datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")
        last_modified = last_modified.replace(tzinfo=pytz.UTC)
        feed_id = f"{company}-{int(last_modified.timestamp())}"

        # Save feed record to database with the Feed model
        feed = Feed.objects.create(
            feed_id=feed_id,
            http_etag=feed_tag,
            http_last_modified=last_modified,
        )

        tables = {
            "agency": "Agency",
            "stops": "Stop",
            "shapes": "Shape",
            "calendar": "Calendar",
            "calendar_dates": "CalendarDate",
            "routes": "Route",
            "trips": "Trip",
            "stop_times": "StopTime",
            "feed_info": "FeedInfo",
        }  # They must be loaded in this order

        # Import and save tables
        for table_name in tables.keys():
            file = f"{table_name}.txt"
            if file in schedule_zip.namelist():
                model = eval(f"{tables[table_name]}")
                fields = [field.name for field in model._meta.fields]
                table = pd.read_csv(
                    schedule_zip.open(file),
                    dtype=str,
                    keep_default_na=False,
                    na_values="",
                )
                table = table[[col for col in fields if col in table.columns]]
                table["feed"] = feed
                objects = [model(**row) for row in table.to_dict(orient="records")]
                model.objects.bulk_create(objects)
                logging.info(f"{file} imported successfully")

    Record.objects.create(
        data_source="https://cdn.mbta.com/MBTA_GTFS.zip",
    )

    return "Fetching Schedule"


@shared_task
def get_vehiclepositions():
    return "Fetching VehiclePositions"


@shared_task
def get_tripupdates():
    return "Fetching TripUpdates"
