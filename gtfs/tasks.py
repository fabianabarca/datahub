from celery import shared_task

import logging
from datetime import datetime, timedelta
import pytz
import zipfile
import io
import json
import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2 as gtfs_rt
from google.protobuf import json_format

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
    providers = Provider.objects.filter(is_active=True)
    for provider in providers:
        vehicle_positions = gtfs_rt.FeedMessage()
        vehicle_positions_response = requests.get(provider.vehicle_positions_url)
        vehicle_positions.ParseFromString(vehicle_positions_response.content)

        feed_message = FeedMessage(
            feed_message_id=f"{provider.code}-vehicle-{vehicle_positions.header.timestamp}",
            provider=provider,
            entity_type="vehicle",
            timestamp=datetime.fromtimestamp(
                int(vehicle_positions.header.timestamp),
                tz=pytz.timezone(provider.timezone),
            ),
            incrementality=vehicle_positions.header.incrementality,
            gtfs_realtime_version=vehicle_positions.header.gtfs_realtime_version,
        )
        feed_message.save()

        vehicle_positions_json = json_format.MessageToJson(
            vehicle_positions, preserving_proto_field_name=True
        )
        vehicle_positions_json = json.loads(vehicle_positions_json)
        vehicle_positions_df = pd.json_normalize(
            vehicle_positions_json["entity"], sep="_"
        )
        vehicle_positions_df.rename(columns={"id": "entity_id"}, inplace=True)
        vehicle_positions_df["feed_message"] = feed_message
        # Drop unnecessary columns
        try:
            vehicle_positions_df.drop(
                columns=["vehicle_multi_carriage_details"],
                inplace=True,
            )
        except:
            pass
        # Fix entity timestamp
        vehicle_positions_df["vehicle_timestamp"] = pd.to_datetime(
            vehicle_positions_df["vehicle_timestamp"].astype(int), unit="s", utc=True
        )
        # Fix trip start date
        vehicle_positions_df["vehicle_trip_start_date"] = pd.to_datetime(
            vehicle_positions_df["vehicle_trip_start_date"], format="%Y%m%d"
        )
        vehicle_positions_df["vehicle_trip_start_date"].fillna(
            datetime.now().date(), inplace=True
        )
        # Fix trip start time
        vehicle_positions_df["vehicle_trip_start_time"] = pd.to_timedelta(
            vehicle_positions_df["vehicle_trip_start_time"]
        )
        vehicle_positions_df["vehicle_trip_start_time"].fillna(
            timedelta(hours=0, minutes=0, seconds=0), inplace=True
        )
        # Fix trip direction
        vehicle_positions_df["vehicle_trip_direction_id"].fillna(-1, inplace=True)
        # Fix current stop sequence
        vehicle_positions_df["vehicle_current_stop_sequence"].fillna(-1, inplace=True)
        # Create vehicle position point
        vehicle_positions_df["vehicle_position_point"] = vehicle_positions_df.apply(
            lambda x: f"POINT ({x.vehicle_position_longitude} {x.vehicle_position_latitude})",
            axis=1,
        )
        # Save to database
        objects = [
            VehiclePosition(**row)
            for row in vehicle_positions_df.to_dict(orient="records")
        ]
        VehiclePosition.objects.bulk_create(objects)

    return "VehiclePositions saved to database"


@shared_task
def get_tripupdates():
    return "Fetching TripUpdates"


@shared_task
def get_alerts():
    return "Fetching Alerts"