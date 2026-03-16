from extract import (
    read_stations_csv,
    read_lines_csv,
    read_boroughs_csv,
    read_zones_csv,
    read_journeys_json
)
from transform_etl import run_etl_transform
from load_postgres import load_transport_report_etl


def main():
    stations_raw = read_stations_csv()
    lines_raw = read_lines_csv()
    boroughs_raw = read_boroughs_csv()
    zones_raw = read_zones_csv()
    journeys_raw = read_journeys_json()

    transport_report = run_etl_transform(
        stations_raw,
        lines_raw,
        boroughs_raw,
        zones_raw,
        journeys_raw
    )

    load_transport_report_etl(transport_report)

    print(f"ETL completed successfully. Loaded {len(transport_report)} rows into transport_report_etl.")


if __name__ == "__main__":
    main()