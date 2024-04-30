from celery import shared_task

import logging
import configparser
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
import requests
import zipfile
import io
import pytz
from .django_data_mapping import django_data_mapping

from .models import *

# Logging configuration
logging.basicConfig(
    filename="schedule.log",
    format="%(levelname)s: %(message)s",
    encoding="utf-8",
    level=logging.INFO,
)

@shared_task
def get_schedule():

    provider = Provider.objects.get(name="MBTA")
    
    # GTFS provider information
    provider_name = provider.name
    schedule_url = provider.schedule_url

    logging.info(
        f"Checking for a new GTFS Schedule feed from {provider_name} at {datetime.now()}. Data source: {schedule_url}"
    )

    # Check if the feed has been updated
    last_feed_tag = {"value": None}
    try:
        last_feed_tag["value"] = (
            Feed.objects.filter(provider=provider)
            .order_by("-retrieved_at")
            .first()
            .http_etag
        )
    except:
        logging.info("No records found in the table 'feeds' for this provider. A new feed will be imported.")

    schedule_check = requests.head(schedule_url)
    feed_tag = schedule_check.headers["ETag"]

    if not feed_tag == last_feed_tag["value"]:
        logging.info(f"New GTFS Schedule feed detected with tag {feed_tag}. Import begins...")

        # Request feed
        schedule_response = requests.get(schedule_url)
        schedule_zip = zipfile.ZipFile(io.BytesIO(schedule_response.content))

        http_last_modified = schedule_check.headers["Last-Modified"]
        http_last_modified = datetime.strptime(http_last_modified, "%a, %d %b %Y %H:%M:%S %Z")
        http_last_modified = http_last_modified.replace(tzinfo=pytz.UTC)
        feed_id = f"{provider_name}-{int(http_last_modified.timestamp())}"
        
        # Save feed record data to database
        try:
            # Save to database with the Feed model
            feed = Feed(
                feed_id=feed_id,
                http_etag=feed_tag,
                http_last_modified=http_last_modified,
                is_current=True,
                provider=provider,
            )
            feed.save()
        except Exception as e:
            logging.error(f"Error saving feed to database: {e}")

        # Save GTFS data to database
        tables = {
            "agency": "Agency",
            "stops": "Stop",
            "shapes": "Shape",
            "calendar": "Calendar",
            "calendar_dates": "CalendarDate",
            "routes": "Route",
            "trips": "Trip",
            #"frequencies": "Frequency",
            "stop_times": "StopTime",
            "feed_info": "FeedInfo",
        }  # They must be loaded in this order

        # Import and save tables
        success = True
        for table_name in tables.keys():
            file = f"{table_name}.txt"
            if file in schedule_zip.namelist():
                model = eval(f"{tables[table_name]}")
                fields = {field.name: django_data_mapping[field.get_internal_type()] for field in model._meta.fields}
                logging.info(f"{model} fields (Python):\n{fields}")
                table = pd.read_csv(schedule_zip.open(file), dtype=fields)
                table = table[[col for col in fields if col in table.columns]]
                logging.info(f"Columns of table {file}:\n{table.columns}")
                logging.info(f"Data types of table {file}:\n{table.dtypes}")
                table["feed"] = feed
                objects = [model(**row) for row in table.to_dict(orient="records")]
                try:
                    model.objects.bulk_create(objects)
                    logging.info(f"File {file} imported successfully")
                    success &= True
                except Exception as e:
                    logging.error(f"Error importing {file}: {e}")
                    success &= False
        if success:
            result = f"New feed imported successfully. Feed ID: {feed_id}"
            logging.info(result)
        else:
            result = "Error importing feed. Check logs for details."
            logging.error(result)
    else:
        result = "No new feed detected. Nothing was imported."
        logging.info(result)

    return result


@shared_task
def get_vehiclepositions():
    return "Fetching VehiclePositions"


@shared_task
def get_tripupdates():
    return "Fetching TripUpdates"
