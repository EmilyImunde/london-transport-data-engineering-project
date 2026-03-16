def clean_text(value):
    if value is None:
        return ""
    return str(value).strip().title()


def clean_stations(stations):
    cleaned_stations = []
    seen_station_ids = set()

    for station in stations:
        station_id = str(station.get("station_id", "")).strip()

        if not station_id:
            continue

        if station_id in seen_station_ids:
            continue

        seen_station_ids.add(station_id)

        cleaned_stations.append({
            "station_id": station_id,
            "station_name": clean_text(station.get("station_name")),
            "borough_id": str(station.get("borough_id", "")).strip(),
            "zone_id": str(station.get("zone_id", "")).strip(),
            "line_id": str(station.get("line_id", "")).strip(),
            "station_type": clean_text(station.get("station_type"))
        })

    return cleaned_stations


def clean_lines(lines):
    cleaned_lines = []
    seen_line_ids = set()

    for line in lines:
        line_id = str(line.get("line_id", "")).strip()

        if not line_id:
            continue

        if line_id in seen_line_ids:
            continue

        seen_line_ids.add(line_id)

        cleaned_lines.append({
            "line_id": line_id,
            "line_name": clean_text(line.get("line_name")),
            "transport_mode": clean_text(line.get("transport_mode")),
            "operator_id": str(line.get("operator_id", "")).strip(),
            "vehicle_type_id": str(line.get("vehicle_type_id", "")).strip()
        })

    return cleaned_lines


def clean_boroughs(boroughs):
    cleaned_boroughs = []
    seen_borough_ids = set()

    for borough in boroughs:
        borough_id = str(borough.get("borough_id", "")).strip()

        if not borough_id:
            continue

        if borough_id in seen_borough_ids:
            continue

        seen_borough_ids.add(borough_id)

        cleaned_boroughs.append({
            "borough_id": borough_id,
            "borough_name": clean_text(borough.get("borough_name")),
            "region_group": clean_text(borough.get("region_group"))
        })

    return cleaned_boroughs


def clean_zones(zones):
    cleaned_zones = []
    seen_zone_ids = set()

    for zone in zones:
        zone_id = str(zone.get("zone_id", "")).strip()

        if not zone_id:
            continue

        if zone_id in seen_zone_ids:
            continue

        seen_zone_ids.add(zone_id)

        cleaned_zones.append({
            "zone_id": zone_id,
            "zone_name": clean_text(zone.get("zone_name")),
            "fare_group": clean_text(zone.get("fare_group"))
        })

    return cleaned_zones

def clean_journeys(journeys):
    cleaned_journeys = []

    for journey in journeys:
        journey_id = str(journey.get("journey_id", "")).strip()
        station_id = str(journey.get("station_id", "")).strip()
        line_id = str(journey.get("line_id", "")).strip()
        passenger_count_value = str(journey.get("passenger_count", "")).strip()
        delay_minutes_value = str(journey.get("delay_minutes", "")).strip()
        journey_date = str(journey.get("journey_date", "")).strip()

        if not journey_id or not station_id or not line_id:
            continue

        try:
            passenger_count = int(passenger_count_value)
            delay_minutes = int(delay_minutes_value)
        except ValueError:
            continue

        cleaned_journeys.append({
            "journey_id": journey_id,
            "station_id": station_id,
            "line_id": line_id,
            "passenger_count": passenger_count,
            "delay_minutes": delay_minutes,
            "journey_date": journey_date,
            "time_band": clean_text(journey.get("time_band")),
            "entry_exit_flag": clean_text(journey.get("entry_exit_flag"))
        })

    return cleaned_journeys


def build_lookup(records, key_field):
    lookup = {}

    for record in records:
        lookup[record[key_field]] = record

    return lookup


def build_transport_report_etl(stations, lines, boroughs, zones, journeys):
    station_lookup = build_lookup(stations, "station_id")
    line_lookup = build_lookup(lines, "line_id")
    borough_lookup = build_lookup(boroughs, "borough_id")
    zone_lookup = build_lookup(zones, "zone_id")

    transport_report = []

    for journey in journeys:
        station = station_lookup.get(journey["station_id"])
        line = line_lookup.get(journey["line_id"])

        if not station or not line:
            continue

        borough = borough_lookup.get(station["borough_id"])
        zone = zone_lookup.get(station["zone_id"])

        transport_report.append({
            "journey_id": journey["journey_id"],
            "journey_date": journey["journey_date"],
            "station_id": station["station_id"],
            "station_name": station["station_name"],
            "borough_id": station["borough_id"],
            "borough_name": borough["borough_name"] if borough else "",
            "zone_id": station["zone_id"],
            "zone_name": zone["zone_name"] if zone else "",
            "line_id": line["line_id"],
            "line_name": line["line_name"],
            "transport_mode": line["transport_mode"],
            "passenger_count": journey["passenger_count"],
            "delay_minutes": journey["delay_minutes"],
            "time_band": journey["time_band"],
            "entry_exit_flag": journey["entry_exit_flag"]
        })

    return transport_report


def run_etl_transform(stations_raw, lines_raw, boroughs_raw, zones_raw, journeys_raw):
    stations_clean = clean_stations(stations_raw)
    lines_clean = clean_lines(lines_raw)
    boroughs_clean = clean_boroughs(boroughs_raw)
    zones_clean = clean_zones(zones_raw)
    journeys_clean = clean_journeys(journeys_raw)

    transport_report = build_transport_report_etl(
        stations_clean,
        lines_clean,
        boroughs_clean,
        zones_clean,
        journeys_clean
    )

    return transport_report