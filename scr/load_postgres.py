import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="london_eng_transport",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

def load_transport_report_etl(records):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM transport_report_etl;")

    insert_query = """
        INSERT INTO transport_report_etl (
            journey_id,
            journey_date,
            station_id,
            station_name,
            borough_id,
            borough_name,
            zone_id,
            zone_name,
            line_id,
            line_name,
            transport_mode,
            passenger_count,
            delay_minutes,
            time_band,
            entry_exit_flag
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    for record in records:
        cursor.execute(
            insert_query,
            (
                record["journey_id"],
                record["journey_date"],
                record["station_id"],
                record["station_name"],
                record["borough_id"],
                record["borough_name"],
                record["zone_id"],
                record["zone_name"],
                record["line_id"],
                record["line_name"],
                record["transport_mode"],
                record["passenger_count"],
                record["delay_minutes"],
                record["time_band"],
                record["entry_exit_flag"]
            )
        )

    connection.commit()
    cursor.close()
    connection.close()

# command for ELT stage

def load_raw_stations(records):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM raw_stations;")

    insert_query = """
        INSERT INTO raw_stations (
            station_id,
            station_name,
            borough_id,
            zone_id,
            line_id,
            station_type
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    for record in records:
        cursor.execute(
            insert_query,
            (
                record.get("station_id"),
                record.get("station_name"),
                record.get("borough_id"),
                record.get("zone_id"),
                record.get("line_id"),
                record.get("station_type")
            )
        )

    connection.commit()
    cursor.close()
    connection.close()



def load_raw_lines(records):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM raw_lines;")

    insert_query = """
        INSERT INTO raw_lines (
            line_id,
            line_name,
            transport_mode,
            operator_id,
            vehicle_type_id,
            service_status,
            snapshot_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    for record in records:
        cursor.execute(
            insert_query,
            (
                record.get("line_id"),
                record.get("line_name"),
                record.get("transport_mode"),
                record.get("operator_id"),
                record.get("vehicle_type_id"),
                record.get("service_status"),
                record.get("snapshot_date")
            )
        )

    connection.commit()
    cursor.close()
    connection.close()


def load_raw_boroughs(records):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM raw_boroughs;")

    insert_query = """
        INSERT INTO raw_boroughs (
            borough_id,
            borough_name,
            region_group,
            population_band,
            avg_daily_ridership_band,
            report_month
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    for record in records:
        cursor.execute(
            insert_query,
            (
                record.get("borough_id"),
                record.get("borough_name"),
                record.get("region_group"),
                record.get("population_band"),
                record.get("avg_daily_ridership_band"),
                record.get("report_month")
            )
        )

    connection.commit()
    cursor.close()
    connection.close()


def load_raw_zones(records):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM raw_zones;")

    insert_query = """
        INSERT INTO raw_zones (
            zone_id,
            zone_name,
            fare_group,
            peak_multiplier,
            status_note,
            report_date
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    for record in records:
        cursor.execute(
            insert_query,
            (
                record.get("zone_id"),
                record.get("zone_name"),
                record.get("fare_group"),
                record.get("peak_multiplier"),
                record.get("status_note"),
                record.get("report_date")
            )
        )

    connection.commit()
    cursor.close()
    connection.close()

def load_raw_journeys(records):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM raw_journeys;")

    insert_query = """
        INSERT INTO raw_journeys (
            journey_id,
            station_id,
            line_id,
            passenger_count,
            delay_minutes,
            journey_date,
            time_band,
            entry_exit_flag
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    for record in records:
        cursor.execute(
            insert_query,
            (
                record.get("journey_id"),
                record.get("station_id"),
                record.get("line_id"),
                record.get("passenger_count"),
                record.get("delay_minutes"),
                record.get("journey_date"),
                record.get("time_band"),
                record.get("entry_exit_flag")
            )
        )

    connection.commit()
    cursor.close()
    connection.close()

from pathlib import Path


def run_sql_file(file_path):
    connection = get_connection()
    cursor = connection.cursor()

    sql_path = Path(file_path)
    sql_content = sql_path.read_text(encoding="utf-8")

    cursor.execute(sql_content)

    connection.commit()
    cursor.close()
    connection.close()

    