from extract import (
    read_stations_csv,
    read_lines_csv,
    read_boroughs_csv,
    read_zones_csv,
    read_journeys_json
)
from load_postgres import (
    load_raw_stations,
    load_raw_lines,
    load_raw_boroughs,
    load_raw_zones,
    load_raw_journeys,
    run_sql_file
)


def main():
    run_sql_file("sql/create_tables.sql")
    stations_raw = read_stations_csv()
    lines_raw = read_lines_csv()
    boroughs_raw = read_boroughs_csv()
    zones_raw = read_zones_csv()
    journeys_raw = read_journeys_json()

    load_raw_stations(stations_raw)
    load_raw_lines(lines_raw)
    load_raw_boroughs(boroughs_raw)
    load_raw_zones(zones_raw)
    load_raw_journeys(journeys_raw)

    run_sql_file("sql/elt_transform.sql")

    print("ELT completed successfully. Raw data loaded and SQL transformations applied.")


if __name__ == "__main__":
    main()

