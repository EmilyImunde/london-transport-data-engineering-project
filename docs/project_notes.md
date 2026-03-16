1. ETL Pipeline Inspection
After running "python src/run_etl.py" the following was reported: ETL completed successfully. Loaded 235 rows into transport_report_etl

2. Data inspection in SQL on "sql/etl_checks.sql":
a) SELECT COUNT(*) FROM transport_report_etl;  count
-------
   235
(1 row)

b) SELECT * FROM transport_report_etl LIMIT 10;
sample extraction:
journey_id | journey_date | station_id |      station_name       | borough_id |      borough_name      | zone_id | zone_name | line_id |     line_name     | transport_mode | passenger_count | delay_minutes | time_ba
nd | entry_exit_flag
------------+--------------+------------+-------------------------+------------+------------------------+---------+-----------+---------+-------------------+----------------+-----------------+---------------+--------
---+-----------------
 J00001     | 2026-02-10   | S0078      | Lewisham Road           | B011       | Greenwich              | Z6      | Zone 6    | L004    | Piccadilly        | Underground    |            1699 |             1 | Midday 
   | Entry
 J00002     | 2026-02-14   | S0113      | Clapham Common Station  | B014       | Brent                  | Z3      | Zone 3    | L015    | Route 149         | Bus            |            1678 |            20 | Am Peak
   | Exit
 J00003     | 2026-02-27   | S0021      | London Bridge Gate      | B006       | Tower Hamlets          | Z6      | Zone 6    | L014    | Route 73          | Bus            |             979 |             5 | Pm Peak
   | Transfer
 J00004     | 2026-02-23   | S0109      | Ealing Broadway Station | B019       | Kensington And Chelsea | Z1      | Zone 1    | L010    | London Overground | Overground     |            1703 |             0 | Pm Peak
   | Transfer
 J00005     | 2026-02-24   | S0017      | Clapham Common Junction | B015       | Croydon                | Z2      | Zone 2    | L009    | Dlr               | Light Rail     |             876 |            15 | Pm Peak
   | Exit
(5 rows)

c) SELECT station_name, SUM(passenger_count) AS total_passengers
FROM transport_report_etl
GROUP BY station_name
ORDER BY total_passengers DESC
LIMIT 10;

london_eng_transport-# LIMIT 10;
      station_name       | total_passengers
-------------------------+------------------
 Acton Gate              |             5636
 Paddington Park         |             4930
 Baker Street Gate       |             4602
 Highbury Station        |             4494
 Tottenham Hale Gate     |             3999
 Canary Wharf Gate       |             3613
 Camden Town Gate        |             3460
 King'S Cross Park       |             3287
 Euston Road             |             2989
 Shepherd'S Bush Central |             2894
(10 rows)





d) SELECT line_name, AVG(delay_minutes) AS avg_delay
FROM transport_report_etl
GROUP BY line_name
ORDER BY avg_delay DESC;

london_eng_transport-# ORDER BY avg_delay DESC;
     line_name     |     avg_delay
-------------------+--------------------
 Dlr               | 9.3500000000000000
 Route 73          | 9.1052631578947368
 London Overground | 8.5000000000000000
 Northern          | 8.4444444444444444
 Central           | 7.6111111111111111
 Route 149         | 6.6500000000000000
 Elizabeth Line    | 6.5333333333333333
 District          | 6.4545454545454545
 Tramlink          | 6.2105263157894737
 Jubilee           | 6.1333333333333333
 Circle            | 5.8181818181818182
 Route 24          | 5.5000000000000000
 Piccadilly        | 5.4583333333333333
 Route 38          | 4.8666666666666667
 Victoria          | 3.8333333333333333
 Bakerloo          | 3.3333333333333333
(16 rows)

e) SELECT borough_name, SUM(passenger_count) AS total_passengers
FROM transport_report_etl
GROUP BY borough_name
ORDER BY total_passengers DESC;

      borough_name      | total_passengers
------------------------+------------------
 Richmond Upon Thames   |            17390
 Hammersmith And Fulham |            15971
 Hackney                |            15114
 Islington              |            14095
 Brent                  |            13671
 Bromley                |            12949
 Newham                 |            12908
 Lambeth                |            12535
 Greenwich              |            11628
 Lewisham               |             9440
 Tower Hamlets          |             9424
 Barnet                 |             9115
 Southwark              |             8655
 Camden                 |             7921
 Croydon                |             7515
 Ealing                 |             6689
 Kensington And Chelsea |             5613
 Wandsworth             |             5602
 Haringey               |             5234
 Westminster            |             3890
(20 rows)




4. WHICH FILES WERE USED IN THE MAIN ETL JOIN
stations.csc by station_id
lines.csv  by line_id
boroughs.csv  by borough_id
zones.csv by zone_id



5. WHAT KINDS OF DATA QUALITY PROBLEMS WERE FOUND
boroughs.csv
i) Some names were all in UPPERCACE- e.g. TOWER HAMLETS, 
i) Missing borough_id e.g for Haringey (borough_name)
ii)Missing borough_name e.g for borough_id B009

stations.csv
i) Missing Sattion name e.g for station_id S0026
ii) Some names were all in UPPERCACE- e.g. PADDINGTON CENTRAL
iii)Missing zone_id e.g for station_id S0112

lines.csv
i) Some lines were written differently, e.g. DLR, dlr



6. WHICH RECORDS WERE SKIPPED AND WHY
The records where Key_id was missing. e.g. Zone_id or borough_id. This would make the JOIN inaccurate


7. WHAT THE FINAL REPORTING TABLE REPRESENTS
 1.	Passenger Traffic Summary= Total passenger count across all journeys. To show overall transport demand
2.	Passenger Distribution by Transport Mode= Shows which transport system is most used.
3.	Busiest Stations= Identify stations with the highest passenger activity, Most crowded stations
4.	Passenger Traffic by Borough= Shows which borough has the highest transport usage. Will show high-demand boroughs
5.	Peak Time Travel Analysis= Identify when the system is busiest. Comparison between AM Peak vs PM Peak vs Midday demand
6.	Delay Analysis= Measure system reliability. By showing which transport mode experiences the most delays
7.	Highest Delay Routes= Identify problematic routes. Routes needing improvement
8.	Zone-Based Travel Demand= Analyse Passenger distribution accros zones. To show which zones have the most transport usage

