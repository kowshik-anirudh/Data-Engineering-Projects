# Trip Analytics: End-to-End Data Engineering on GCP with Mage

An end-to-end batch pipeline that takes raw ride-hail/taxi trip records, models them into a star schema, loads them into BigQuery, and serves an analytics dashboard in Looker Studio.

## Architecture

```mermaid
flowchart LR
    A[Trip records CSV] --> B[Mage on Compute Engine<br/>extract]
    B --> C[Mage transform<br/>pandas star schema]
    C --> D[(BigQuery<br/>fact + dimension tables)]
    D --> E[Analytics table<br/>SQL joins]
    E --> F[Looker Studio dashboard]
```

## Dataset

NYC TLC yellow taxi trip records: pickup and drop-off times and locations, trip distance, itemized fares, rate codes, payment types, and passenger counts. A copy of the data used is in [`data/lyft_data.csv`](Lyft-etl-pipeline-data-engineering-project-main/data/lyft_data.csv).

- Source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Data dictionary: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

## Data model

A star schema built in pandas ([`transform.py`](Lyft-etl-pipeline-data-engineering-project-main/mage-files/transform.py)):

- **fact_table**: one row per trip, with fare components (fare, extra, MTA tax, tip, tolls, surcharge, total) and keys to each dimension
- **datetime_dim**: pickup/drop-off timestamps broken into hour, day, month, year, weekday
- **passenger_count_dim**, **trip_distance_dim**
- **rate_code_dim**, **payment_type_dim**: codes mapped to readable names
- **pickup_location_dim**, **dropoff_location_dim**: latitude/longitude

[`analytics_query.sql`](Lyft-etl-pipeline-data-engineering-project-main/analytics_query.sql) joins these back into a single analytics table for the dashboard.

## Pipeline (Mage)

| Step | File | What it does |
|---|---|---|
| Extract | [`extract.py`](Lyft-etl-pipeline-data-engineering-project-main/mage-files/extract.py) | Loads the trip CSV (from this repo by default, or `LYFT_DATA_URL`) |
| Transform | [`transform.py`](Lyft-etl-pipeline-data-engineering-project-main/mage-files/transform.py) | Builds the fact and dimension tables |
| Load | [`load.py`](Lyft-etl-pipeline-data-engineering-project-main/mage-files/load.py) | Writes every table to BigQuery |

## Running it

1. Create a GCP project, a BigQuery dataset (e.g. `lyft_data_engineering`), and a service account with BigQuery access.
2. Create a Compute Engine VM and install Mage and the Google Cloud libraries (see [`commands.txt`](Lyft-etl-pipeline-data-engineering-project-main/commands.txt)).
3. Add the service account credentials to Mage's `io_config.yaml`.
4. Set `GCP_PROJECT_ID` (and optionally `BQ_DATASET`) and run the pipeline.
5. Run `analytics_query.sql` (replacing `your-gcp-project`) and connect the analytics table to Looker Studio.

## Tech

Python · pandas · Mage · Google Compute Engine · BigQuery · SQL · Looker Studio

## Acknowledgements

This project was built by following Darshil Parmar's ("Data with Darshil") Uber data engineering tutorial, and the original README structure was adapted from [snehalsmalladi/Lyft-Analytics-Data-Engineering-GCP-Mage-ETL](https://github.com/snehalsmalladi/Lyft-Analytics-Data-Engineering-GCP-Mage-ETL). The pipeline here runs in my own GCP environment, and the target project and dataset are configurable.
