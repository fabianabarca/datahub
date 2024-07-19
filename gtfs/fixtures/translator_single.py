import csv
import json


# The CSV input data
csv_data = """fare_id,route_id,origin_id,destination_id
no_tarifa,UCR_L1,UCR_0,UCR_0
no_tarifa,UCR_L2,UCR_1,UCR_1"""

# Split the CSV data into lines and read it
csv_reader = csv.DictReader(csv_data.splitlines())

# Convert CSV to a structured JSON format
json_data = []
for i, row in enumerate(csv_reader, start=1):
    json_data.append({
        "model": "gtfs.FareRule",
        "pk": i,
        "fields": {
            "feed": '1234',
            "fare_id": row['fare_id'],
            "route_id": row['route_id'],
            "origin_id": row['origin_id'],
            "destination_id": row['destination_id']
        }
    })

# Convert the structured data into JSON format
json_output = json.dumps(json_data, indent=4)

# Save the output in .json file
with open('FareRule.json', 'w',encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)