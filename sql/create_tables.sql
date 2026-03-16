CREATE TABLE IF NOT EXISTS raw_stations (
    station_id TEXT,
    station_name TEXT,
    borough_id TEXT,
    zone_id TEXT,
    line_id TEXT,
    station_type TEXT
);

CREATE TABLE IF NOT EXISTS raw_lines (
    line_id TEXT,
    line_name TEXT,
    transport_mode TEXT,
    operator_id TEXT,
    vehicle_type_id TEXT,
    service_status TEXT,
    snapshot_date TEXT
);

CREATE TABLE IF NOT EXISTS raw_boroughs (
    borough_id TEXT,
    borough_name TEXT,
    region_group TEXT,
    population_band TEXT,
    avg_daily_ridership_band TEXT,
    report_month TEXT
);

CREATE TABLE IF NOT EXISTS raw_zones (
    zone_id TEXT,
    zone_name TEXT,
    fare_group TEXT,
    peak_multiplier TEXT,
    status_note TEXT,
    report_date TEXT
);

CREATE TABLE IF NOT EXISTS raw_journeys (
    journey_id TEXT,
    station_id TEXT,
    line_id TEXT,
    passenger_count TEXT,
    delay_minutes TEXT,
    journey_date TEXT,
    time_band TEXT,
    entry_exit_flag TEXT
);

CREATE TABLE IF NOT EXISTS transport_report_elt (
    journey_id TEXT,
    journey_date DATE,
    station_id TEXT,
    station_name TEXT,
    borough_id TEXT,
    borough_name TEXT,
    zone_id TEXT,
    zone_name TEXT,
    line_id TEXT,
    line_name TEXT,
    transport_mode TEXT,
    passenger_count INTEGER,
    delay_minutes INTEGER,
    time_band TEXT,
    entry_exit_flag TEXT
);