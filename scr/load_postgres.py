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


