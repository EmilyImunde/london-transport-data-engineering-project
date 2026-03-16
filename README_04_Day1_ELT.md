# Day 1 ELT Tasks  - updated 
## London Transport Data Engineering Project

Welcome to the **ELT part of Day 1**.

In this file, you will build the **local ELT version** of the London Transport Data Engineering Project.

ELT means:

- **Extract**
- **Load**
- **Transform**

That means your job in this part is to:

1. extract raw data from source files
2. load the raw data into PostgreSQL first
3. transform the data later inside PostgreSQL using SQL

This is also a real and important data engineering pattern.

In many modern data platforms, teams use ELT because they want to preserve raw data first and perform transformations inside the database, warehouse, or analytics platform.

So even though this project is guided, the architecture itself is realistic.

---

# 1. Day 1 ELT objective

Your goal in this part is to build a working ELT pipeline that uses London transport raw data and produces a clean reporting table in PostgreSQL.

By the end of this ELT task file, you should have:

- loaded selected raw source files into PostgreSQL raw tables
- preserved the raw data in its original form
- transformed the data using SQL
- created a final reporting table
- validated the result with SQL queries

---

# 2. Important note before starting

This project contains **10 raw source files**, but like the ETL version, the main Day 1 ELT reporting output will focus on the most important files for the first reporting layer:

- `stations.csv`
- `lines.csv`
- `journeys.json`
- `boroughs.csv`
- `zones.csv`

The other files still belong to the raw project environment and remain important for future extensions, validation, enrichment, and later project stages.

That is realistic.

Not every file has to be used equally in the first reporting layer.

---

# 3. What final ELT output are we building today?

For Day 1 ELT, the final PostgreSQL table will be:

```text
transport_report_elt
````

This table should help answer business questions such as:

* Which stations are busiest?
* Which lines carry the highest passenger traffic?
* Which boroughs show the most activity?
* Which zones appear most often?
* Which journeys have delays?

This is the same business goal as ETL, but the architecture is different.

---

# 4. ELT flow for Day 1

Here is the flow you are building:

```text
Raw source files → Python extraction → Load raw data into PostgreSQL → Transform inside PostgreSQL with SQL
```

More specifically:

```text
stations.csv
lines.csv
journeys.json
boroughs.csv
zones.csv
      ↓
Python extraction
      ↓
raw_stations
raw_lines
raw_journeys
raw_boroughs
raw_zones
      ↓
SQL transformation inside PostgreSQL
      ↓
transport_report_elt
```

Keep this order in mind.

The transformation happens **after** the raw data is loaded into PostgreSQL.

That is what makes this ELT.

---

# 5. Step 1 - Create the raw and final PostgreSQL tables

## Your task

Open:

```text
sql/create_tables.sql
```

and add these table definitions below your ETL table section:

```sql
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
```

## Why this matters

In the ELT version, we preserve the raw source data first.

That is why the raw tables mostly use `TEXT`.

This makes loading easier and lets PostgreSQL perform the real transformation later.

This is very common in ELT-style thinking.

---

# 6. Step 2 - Reuse the extraction layer

## Your task

You can reuse the extraction functions from `src/extract.py`.

For Day 1 ELT, you should already have or keep these functions:

* `read_stations_csv()`
* `read_lines_csv()`
* `read_boroughs_csv()`
* `read_zones_csv()`
* `read_journeys_json()`

If needed, your `src/extract.py` should already contain:

```python
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
```

## Why this matters

The extraction layer does not change much between ETL and ELT.

The major difference is what happens **after extraction**.

---

# 7. Step 3 - Prepare the PostgreSQL connection

## Your task

Open:

```text
src/load_postgres.py
```

and make sure it contains this function:

```python
import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="transport_project",
        user="postgres",
        password="your_password",
        host="localhost",
        port="5432"
    )
```

## Important note

Replace `"your_password"` with your real PostgreSQL password.

---

# 8. Step 4 - Create the raw station loader

## Your task

In `src/load_postgres.py`, add this function:

```python
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
```

## Why this matters

In ELT, we load the station data in its raw form first.

We are not cleaning it yet.

That is intentional.

---

# 9. Step 5 - Create the raw line loader

## Your task

Still in `src/load_postgres.py`, add:

```python
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
```

## Why this matters

Lines are also loaded raw first.

This preserves the original export values before transformation.

---

# 10. Step 6 - Create the raw borough loader

## Your task

Add:

```python
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
```

---

# 11. Step 7 - Create the raw zone loader

## Your task

Add:

```python
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
```

---

# 12. Step 8 - Create the raw journey loader

## Your task

Add:

```python
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
```

## Why this matters

Journeys are the main event-style data, and in the ELT version we deliberately preserve them in raw form first.

Even invalid numeric values can enter the raw table.

The transformation step will decide what to keep.

---

# 13. Step 9 - Add a SQL file runner helper

## Your task

Still in `src/load_postgres.py`, add this helper:

```python
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
```

## Why this matters

In real engineering work, SQL transformations are often stored in separate `.sql` files.

That makes them:

* easier to read
* easier to review
* easier to maintain

That is a good professional habit.

---

# 14. Step 10 - Create the ELT transformation SQL file

## Your task

Open:

```text
sql/elt_transform.sql
```

and begin with this reset statement:

```sql
DELETE FROM transport_report_elt;
```

## Why this matters

This clears the previous transformed result before inserting a fresh one.

That prevents duplicate output from multiple runs.

---

# 15. Step 11 - Write the corrected main ELT transformation query

## Your task

Now add the corrected ELT transformation logic below.

```sql
DELETE FROM transport_report_elt;

WITH dedup_stations AS (
    SELECT DISTINCT ON (station_id)
        station_id,
        station_name,
        borough_id,
        zone_id,
        line_id,
        station_type
    FROM raw_stations
    WHERE station_id IS NOT NULL
      AND TRIM(station_id) <> ''
    ORDER BY station_id
),
dedup_lines AS (
    SELECT DISTINCT ON (line_id)
        line_id,
        line_name,
        transport_mode,
        operator_id,
        vehicle_type_id
    FROM raw_lines
    WHERE line_id IS NOT NULL
      AND TRIM(line_id) <> ''
    ORDER BY line_id
),
dedup_boroughs AS (
    SELECT DISTINCT ON (borough_id)
        borough_id,
        borough_name,
        region_group
    FROM raw_boroughs
    WHERE borough_id IS NOT NULL
      AND TRIM(borough_id) <> ''
    ORDER BY borough_id
),
dedup_zones AS (
    SELECT DISTINCT ON (zone_id)
        zone_id,
        zone_name,
        fare_group
    FROM raw_zones
    WHERE zone_id IS NOT NULL
      AND TRIM(zone_id) <> ''
    ORDER BY zone_id
)
INSERT INTO transport_report_elt (
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
SELECT
    rj.journey_id,
    CAST(rj.journey_date AS DATE) AS journey_date,
    ds.station_id,
    INITCAP(TRIM(ds.station_name)) AS station_name,
    ds.borough_id,
    INITCAP(TRIM(db.borough_name)) AS borough_name,
    ds.zone_id,
    INITCAP(TRIM(dz.zone_name)) AS zone_name,
    dl.line_id,
    INITCAP(TRIM(dl.line_name)) AS line_name,
    INITCAP(TRIM(dl.transport_mode)) AS transport_mode,
    CAST(rj.passenger_count AS INTEGER) AS passenger_count,
    CAST(rj.delay_minutes AS INTEGER) AS delay_minutes,
    INITCAP(TRIM(rj.time_band)) AS time_band,
    INITCAP(TRIM(rj.entry_exit_flag)) AS entry_exit_flag
FROM raw_journeys rj
JOIN dedup_stations ds
    ON rj.station_id = ds.station_id
JOIN dedup_lines dl
    ON rj.line_id = dl.line_id
LEFT JOIN dedup_boroughs db
    ON ds.borough_id = db.borough_id
LEFT JOIN dedup_zones dz
    ON ds.zone_id = dz.zone_id
WHERE rj.journey_id IS NOT NULL
  AND TRIM(rj.journey_id) <> ''
  AND rj.station_id IS NOT NULL
  AND TRIM(rj.station_id) <> ''
  AND rj.line_id IS NOT NULL
  AND TRIM(rj.line_id) <> ''
  AND rj.passenger_count ~ '^[0-9]+$'
  AND rj.delay_minutes ~ '^[0-9]+$'
  AND rj.journey_date ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$';
```

## Why this matters

This version fixes the duplication issue in the ELT pipeline.

The raw reference tables contain repeated records for the same business keys like:

* `station_id`
* `line_id`
* `borough_id`
* `zone_id`

If you join directly to those raw tables, PostgreSQL can multiply rows and produce a final table that is much larger than expected.

By creating deduplicated lookup layers first, the final join becomes correct and stable.

> **Update note:** This step was corrected after duplicate-row behavior was observed by [@Alan](https://github.com/alan8burke) in `transport_report_elt`. The SQL now deduplicates reference tables before joining.

---

# 16. Step 12 - Why the deduplication step matters

## Your task

Study these CTEs carefully:

```sql
WITH dedup_stations AS (...),
dedup_lines AS (...),
dedup_boroughs AS (...),
dedup_zones AS (...)
```

## Why this matters

These CTEs act like a temporary cleaned reference layer inside PostgreSQL.

They make sure that each business key appears only once before the final joins happen.

Without this step, the join can multiply rows and produce incorrect reporting output.

So this is one of the most important parts of the corrected ELT design.

> **Update note:** This explanation was added to clarify why the corrected SQL uses `DISTINCT ON` before joining.

---

# 17. Step 13 - Create reporting queries

## Your task

Open:

```text
sql/reporting_queries.sql
```

and add these validation queries:

```sql
SELECT COUNT(*) FROM transport_report_elt;
```

```sql
SELECT * FROM transport_report_elt LIMIT 10;
```

```sql
SELECT station_name, SUM(passenger_count) AS total_passengers
FROM transport_report_elt
GROUP BY station_name
ORDER BY total_passengers DESC
LIMIT 10;
```

```sql
SELECT line_name, AVG(delay_minutes) AS avg_delay
FROM transport_report_elt
GROUP BY line_name
ORDER BY avg_delay DESC;
```

```sql
SELECT borough_name, SUM(passenger_count) AS total_passengers
FROM transport_report_elt
GROUP BY borough_name
ORDER BY total_passengers DESC;
```

## Why this matters

These queries help you validate whether the final reporting result makes business sense.

A pipeline is not complete until you confirm the output is usable.

---

# 18. Step 14 - Create the ELT runner script

## Your task

Open:

```text
src/run_elt.py
```

and add this code:

```python
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
```

## Why this matters

This runner shows the ELT flow clearly:

1. extract raw data
2. load raw tables into PostgreSQL
3. transform inside PostgreSQL with SQL

That is exactly the ELT design.

---

# 19. Step 15 - Run the ELT pipeline

## Your task

From the project root, run:

```bash
python src/run_elt.py
```

## What you should expect

If everything works, you should see something like:

```text
ELT completed successfully. Raw data loaded and SQL transformations applied.
```

If you get errors, check:

* PostgreSQL connection details
* whether the tables were created first
* whether the files are in `data/raw/`
* whether the SQL file contains syntax mistakes
* whether you are running from the project root

This is normal engineering debugging work.

---

# 20. Step 16 - Validate the raw tables first

## Your task

Before checking the final report table, inspect the raw tables.

Run these queries in PostgreSQL:

```sql
SELECT * FROM raw_stations LIMIT 10;
```

```sql
SELECT * FROM raw_lines LIMIT 10;
```

```sql
SELECT * FROM raw_boroughs LIMIT 10;
```

```sql
SELECT * FROM raw_zones LIMIT 10;
```

```sql
SELECT * FROM raw_journeys LIMIT 10;
```

## Why this matters

In ELT, the raw layer is an important and intentional part of the architecture.

You should confirm that the raw source data was preserved correctly before transformation.

---

# 21. Step 17 - Validate the final ELT reporting table

## Your task

Now inspect the final result:

```sql
SELECT COUNT(*) FROM transport_report_elt;
```

```sql
SELECT * FROM transport_report_elt LIMIT 10;
```

```sql
SELECT station_name, SUM(passenger_count) AS total_passengers
FROM transport_report_elt
GROUP BY station_name
ORDER BY total_passengers DESC
LIMIT 10;
```

```sql
SELECT line_name, AVG(delay_minutes) AS avg_delay
FROM transport_report_elt
GROUP BY line_name
ORDER BY avg_delay DESC;
```

```sql
SELECT borough_name, SUM(passenger_count) AS total_passengers
FROM transport_report_elt
GROUP BY borough_name
ORDER BY total_passengers DESC;
```

## Why this matters

This final reporting table is the business-ready result of your ELT pipeline.

You should make sure that:

* the joins worked
* the text values were cleaned
* the numeric conversions succeeded
* the business summary looks reasonable

---

# 22. Step 18 - Write project notes for ELT

## Your task

Open:

```text
docs/project_notes.md
```

and add notes about:

* which raw tables were created
* what kinds of bad data were filtered out in SQL
* how the ELT design differs from ETL
* what the final `transport_report_elt` table represents

## Why this matters

This strengthens your project documentation and helps you explain your work later.

That is important for both learning and portfolio value.

---

# 23. Step 19 - Commit and push your ELT progress

## Your task

After completing the ELT part, push your work.

Example:

```bash
git add .
git commit -m "Complete Day 1 ELT pipeline"
git push
```

## Why this matters

Your public GitHub repository is part of your professional project story.

Keep it updated and organized.

---

# 24. What makes this ELT version realistic

This ELT design reflects real engineering habits such as:

* preserving raw source data first
* loading raw exports into a database layer
* transforming later with SQL
* filtering bad values during SQL transformation
* producing final reporting tables inside PostgreSQL

That is why this project should be treated seriously.

The code is guided, but the architecture is real.

---

# 25. Compare ELT with ETL

## Your task

Pause and compare the two versions.

### In ETL

* Python reads the raw files
* Python cleans and joins the data
* PostgreSQL receives the final clean result

### In ELT

* Python reads the raw files
* PostgreSQL receives the raw data first
* SQL in PostgreSQL performs the cleaning and joining later

## Why this matters

This comparison is one of the most important learning goals of Day 1.

You are not just building two scripts.

You are learning two real pipeline architectures.

---

# 26. What you should understand after finishing

By the end of this ELT part, you should understand that:

* ELT means load before transform
* raw data is intentionally preserved in PostgreSQL
* SQL performs the main transformation logic in this version
* bad rows can be filtered during SQL transformation
* the order of the pipeline defines the architecture

That is the core learning goal.

---

# 27. Final Day 1 reminder

At the end of Day 1, you should now have:

* a public GitHub repository
* the full Day 1 project structure
* the 10 raw data files
* a completed ETL version
* a completed ELT version
* checkpoint answers
* project notes
* multiple commits showing your progress

That is a strong and serious Day 1 achievement.

---

# 28. Final message

Treat this ELT part like real junior data engineering work.

The goal is not only to make SQL run.

The goal is to understand how raw transport data can be preserved first and transformed later inside PostgreSQL in a structured ELT workflow.

That is a real data engineering pattern, and learning it now will help you greatly in later stages of the course.



