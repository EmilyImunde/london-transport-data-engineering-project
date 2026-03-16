import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

RAW_DATA_FOLDER = Path("data") / "raw"

def read_csv_file(filename):
    file_path = RAW_DATA_FOLDER / filename
    records = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)

    return records

def read_json_file(filename):
    file_path = RAW_DATA_FOLDER / filename

    with open(file_path, mode="r", encoding="utf-8") as file:
        records = json.load(file)

    return records

def read_schedules_xml():
    file_path = RAW_DATA_FOLDER / "schedules.xml"
    tree = ET.parse(file_path)
    root = tree.getroot()

    schedules = []

    for schedule in root.findall("schedule"):
        schedules.append({
            "schedule_id": schedule.findtext("schedule_id", default=""),
            "station_id": schedule.findtext("station_id", default=""),
            "line_id": schedule.findtext("line_id", default=""),
            "planned_start_time": schedule.findtext("planned_start_time", default=""),
            "planned_end_time": schedule.findtext("planned_end_time", default=""),
            "service_day": schedule.findtext("service_day", default=""),
            "status_note": schedule.findtext("status_note", default="")
        })

    return schedules


def read_stations_csv():
    return read_csv_file("stations.csv")


def read_lines_csv():
    return read_csv_file("lines.csv")


def read_boroughs_csv():
    return read_csv_file("boroughs.csv")


def read_zones_csv():
    return read_csv_file("zones.csv")


def read_journeys_json():
    return read_json_file("journeys.json")

if __name__ == "__main__":
    stations = read_stations_csv()
    lines = read_lines_csv()
    boroughs = read_boroughs_csv()
    zones = read_zones_csv()
    journeys = read_journeys_json()
    schedules = read_schedules_xml()

    print("Stations:", len(stations))
    print("Lines:", len(lines))
    print("Boroughs:", len(boroughs))
    print("Zones:", len(zones))
    print("Journeys:", len(journeys))
    print("Schedules:", len(schedules))