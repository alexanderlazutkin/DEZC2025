- Course homework page: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/04-analytics-engineering/homework.md
- Course materials: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/README.md
- Due date: 25.02.2025 02:00 (local time)



## Module 4 Homework 
For this homework, you will need the following datasets:
- [Green Taxi dataset (2019 and 2020)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green)
- [Yellow Taxi dataset (2019 and 2020)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow)
- [For Hire Vehicle dataset (2019)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv)
### Before you start
1. Make sure you, **at least**, have them in GCS with a External Table **OR** a Native Table - use whichever method you prefer to accomplish that (Workflow Orchestration with [pandas-gbq](https://cloud.google.com/bigquery/docs/samples/bigquery-pandas-gbq-to-gbq-simple), [dlt for gcs](https://dlthub.com/docs/dlt-ecosystem/destinations/filesystem), [dlt for BigQuery](https://dlthub.com/docs/dlt-ecosystem/destinations/bigquery), [gsutil](https://cloud.google.com/storage/docs/gsutil), etc)
2. You should have exactly `7,778,101` records in your Green Taxi table
3. You should have exactly `109,047,518` records in your Yellow Taxi table
4. You should have exactly `43,244,696` records in your FHV table
5. Build the staging models for green/yellow as shown in [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/f3306a8ab25ac8ea79514ccf8744d468887ba75d/04-analytics-engineering/taxi_rides_ny/models/staging)
6. Build the dimension/fact for taxi_trips joining with `dim_zones` as shown in [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/f3306a8ab25ac8ea79514ccf8744d468887ba75d/04-analytics-engineering/taxi_rides_ny/models/core/fact_trips.sql)
**Note**: If you don't have access to GCP, you can spin up a local Postgres instance and ingest the datasets above



### Question 1: Understanding dbt model resolution
Provided you've got the following sources.yaml

```yaml
version: 2

sources:
  - name: raw_nyc_tripdata
    database: "{{ env_var('DBT_BIGQUERY_PROJECT', 'dtc_zoomcamp_2025') }}"
    schema:   "{{ env_var('DBT_BIGQUERY_SOURCE_DATASET', 'raw_nyc_tripdata') }}"
    tables:
      - name: ext_green_taxi
      - name: ext_yellow_taxi
```

with the following env variables setup where `dbt` runs:
```shell
export DBT_BIGQUERY_PROJECT=myproject
export DBT_BIGQUERY_DATASET=my_nyc_tripdata
```
What does this .sql model compile to?
```sql
select * 
from {{ source('raw_nyc_tripdata', 'ext_green_taxi' ) }}
```

- `select * from dtc_zoomcamp_2025.raw_nyc_tripdata.ext_green_taxi`
- `select * from dtc_zoomcamp_2025.my_nyc_tripdata.ext_green_taxi`
- `select * from myproject.raw_nyc_tripdata.ext_green_taxi`
- `select * from myproject.my_nyc_tripdata.ext_green_taxi`
- `select * from dtc_zoomcamp_2025.raw_nyc_tripdata.green_taxi`
#### Answer:  
- `select * from myproject.my_nyc_tripdata.ext_green_taxi`
#### Solution
- The environment variable `DBT_BIGQUERY_PROJECT` is set to `myproject`, so `database` resolves to `myproject`
- The environment variable `DBT_BIGQUERY_DATASET` is set to `my_nyc_tripdata`, so `schema` resolves to `my_nyc_tripdata`
- The table name is `ext_green_taxi`, as specified in the `sources.yaml`


### Question 2: dbt Variables & Dynamic Models

Say you have to modify the following dbt_model (`fct_recent_taxi_trips.sql`) to enable Analytics Engineers to dynamically control the date range.
- In development, you want to process only **the last 7 days of trips**
- In production, you need to process **the last 30 days** for analytics
```sql
select *
from {{ ref('fact_taxi_trips') }}
where pickup_datetime >= CURRENT_DATE - INTERVAL '30' DAY
```
What would you change to accomplish that in a such way that command line arguments takes precedence over ENV_VARs, which takes precedence over DEFAULT value?

- Add `ORDER BY pickup_datetime DESC` and `LIMIT {{ var("days_back", 30) }}`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", 30) }}' DAY`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", "30") }}' DAY`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", var("days_back", "30")) }}' DAY`
#### Answer:  
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY`
#### Solution
- Precedence logic:
    - **Command-line arguments**: When running dbt, you can pass a value for `days_back` using the `--vars` flag, e.g., `dbt run --vars '{"days_back": 7}'`. This takes the highest precedence.
    - **Environment variables**: If no command-line argument is provided, dbt will check for the `DAYS_BACK` environment variable. This is useful for setting defaults in different environments (e.g., development vs. production).
    - **Default value**: If neither a command-line argument nor an environment variable is provided, the default value of `30` will be used.


### Question 3: dbt Data Lineage and Execution

Considering the data lineage below and that taxi_zone_lookup is the **only** materialization build (from a .csv seed file):
[![image](https://github.com/DataTalksClub/data-engineering-zoomcamp/raw/f3306a8ab25ac8ea79514ccf8744d468887ba75d/cohorts/2025/04-analytics-engineering/homework_q2.png)](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/f3306a8ab25ac8ea79514ccf8744d468887ba75d/cohorts/2025/04-analytics-engineering/homework_q2.png)

Select the option that does **NOT** apply for materializing `fct_taxi_monthly_zone_revenue`:
- `dbt run`
- `dbt run --select +models/core/dim_taxi_trips.sql+ --target prod`
- `dbt run --select +models/core/fct_taxi_monthly_zone_revenue.sql`
- `dbt run --select +models/core/`
- `dbt run --select models/staging/+`
#### Answer:  
- `dbt run --select models/staging/+` 


### Question 4: dbt Macros and Jinja
Consider you're dealing with sensitive data (e.g.: [PII](https://en.wikipedia.org/wiki/Personal_data)), that is **only available to your team and very selected few individuals**, in the `raw layer` of your DWH (e.g: a specific BigQuery dataset or PostgreSQL schema),

- Among other things, you decide to obfuscate/masquerade that data through your staging models, and make it available in a different schema (a `staging layer`) for other Data/Analytics Engineers to explore
- And **optionally**, yet another layer (`service layer`), where you'll build your dimension (`dim_`) and fact (`fct_`) tables (assuming the [Star Schema dimensional modeling](https://www.databricks.com/glossary/star-schema)) for Dashboarding and for Tech Product Owners/Managers
You decide to make a macro to wrap a logic around it:
```sql
{% macro resolve_schema_for(model_type) -%}
    {%- set target_env_var = 'DBT_BIGQUERY_TARGET_DATASET'  -%}
    {%- set stging_env_var = 'DBT_BIGQUERY_STAGING_DATASET' -%}
    {%- if model_type == 'core' -%} {{- env_var(target_env_var) -}}
    {%- else -%}                    {{- env_var(stging_env_var, env_var(target_env_var)) -}}
    {%- endif -%}
{%- endmacro %}
```

And use on your staging, dim_ and fact_ models as:
```sql
{{ config(
    schema=resolve_schema_for('core'), 
) }}
```

That all being said, regarding macro above, **select all statements that are true to the models using it**:

- Setting a value for `DBT_BIGQUERY_TARGET_DATASET` env var is mandatory, or it'll fail to compile
- Setting a value for `DBT_BIGQUERY_STAGING_DATASET` env var is mandatory, or it'll fail to compile
- When using `core`, it materializes in the dataset defined in `DBT_BIGQUERY_TARGET_DATASET`
- When using `stg`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`
- When using `staging`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`
#### Answer:  
- Setting a value for `DBT_BIGQUERY_TARGET_DATASET` env var is mandatory, or it'll fail to compile
- When using `core`, it materializes in the dataset defined in `DBT_BIGQUERY_TARGET_DATASET`
- When using `stg`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`
- When using `staging`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`


## Serious SQL
Alright, in module 1, you had a SQL refresher, so now let's build on top of that with some serious SQL.
These are not meant to be easy - but they'll boost your SQL and Analytics skills to the next level.  
So, without any further do, let's get started...
You might want to add some new dimensions `year` (e.g.: 2019, 2020), `quarter` (1, 2, 3, 4), `year_quarter` (e.g.: `2019/Q1`, `2019-Q2`), and `month` (e.g.: 1, 2, ..., 12), **extracted from pickup_datetime**, to your `fct_taxi_trips` OR `dim_taxi_trips.sql` models to facilitate filtering your queries

### Question 5: Taxi Quarterly Revenue Growth
4. Create a new model `fct_taxi_trips_quarterly_revenue.sql`
5. Compute the Quarterly Revenues for each year for based on `total_amount`
6. Compute the Quarterly YoY (Year-over-Year) revenue growth

- e.g.: In 2020/Q1, Green Taxi had -12.34% revenue growth compared to 2019/Q1
- e.g.: In 2020/Q4, Yellow Taxi had +34.56% revenue growth compared to 2019/Q4

Considering the YoY Growth in 2020, which were the yearly quarters with the best (or less worse) and worst results for green, and yellow

- green: {best: 2020/Q2, worst: 2020/Q1}, yellow: {best: 2020/Q2, worst: 2020/Q1}
- green: {best: 2020/Q2, worst: 2020/Q1}, yellow: {best: 2020/Q3, worst: 2020/Q4}
- green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q2, worst: 2020/Q1}
- green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q1, worst: 2020/Q2}
- green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q3, worst: 2020/Q4}
#### Answer:  
- green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q1, worst: 2020/Q2}

```sql
SELECT yoy_growth, year, quarter, service_type, total_revenue, prev_year_revenue
FROM `advance-vector-447116-m5.trips_data_all.fct_taxi_trips_quarterly_revenue` 
WHERE year = 2020
ORDER BY yoy_growth DESC
LIMIT 10
```

### Question 6: P97/P95/P90 Taxi Monthly Fare
7. Create a new model `fct_taxi_trips_monthly_fare_p95.sql`
8. Filter out invalid entries (`fare_amount > 0`, `trip_distance > 0`, and `payment_type_description in ('Cash', 'Credit Card')`)
9. Compute the **continous percentile** of `fare_amount` partitioning by service_type, year and and month

Now, what are the values of `p97`, `p95`, `p90` for Green Taxi and Yellow Taxi, in April 2020?

- green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 52.0, p95: 37.0, p90: 25.5}
- green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}
- green: {p97: 40.0, p95: 33.0, p90: 24.5}, yellow: {p97: 52.0, p95: 37.0, p90: 25.5}
- green: {p97: 40.0, p95: 33.0, p90: 24.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}
- green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 52.0, p95: 25.5, p90: 19.0}
#### Answer:  
- green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}

```sql
{{ config(materialized='table') }}  

WITH prepared_trips AS (
    SELECT 
        service_type,
        EXTRACT(YEAR FROM pickup_datetime) AS year,
        EXTRACT(MONTH FROM pickup_datetime) AS month,
        fare_amount
    FROM {{ ref('fact_trips') }}
    WHERE 
        fare_amount > 0 
        AND trip_distance > 0 
        AND payment_type_description IN ('Cash', 'Credit card')
),

percentile_data AS (
    SELECT 
        service_type,
        year,
        month,
        PERCENTILE_CONT(fare_amount, 0.97) OVER (PARTITION BY service_type, year, month) AS fare_p97,
        PERCENTILE_CONT(fare_amount, 0.95) OVER (PARTITION BY service_type, year, month) AS fare_p95,
        PERCENTILE_CONT(fare_amount, 0.90) OVER (PARTITION BY service_type, year, month) AS fare_p90
    FROM prepared_trips
)

SELECT service_type, year, month, fare_p97, fare_p95, fare_p90
FROM percentile_data
GROUP BY service_type, year, month, fare_p97, fare_p95, fare_p90

```

### Question 7: Top #Nth longest P90 travel time Location for FHV
Prerequisites:
- Create a staging model for FHV Data (2019), and **DO NOT** add a deduplication step, just filter out the entries where `where dispatching_base_num is not null`
- Create a core model for FHV Data (`dim_fhv_trips.sql`) joining with `dim_zones`. Similar to what has been done [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/f3306a8ab25ac8ea79514ccf8744d468887ba75d/04-analytics-engineering/taxi_rides_ny/models/core/fact_trips.sql)
- Add some new dimensions `year` (e.g.: 2019) and `month` (e.g.: 1, 2, ..., 12), based on `pickup_datetime`, to the core model to facilitate filtering for your queries
Now...
1. Create a new model `fct_fhv_monthly_zone_traveltime_p90.sql`
2. For each record in `dim_fhv_trips.sql`, compute the [timestamp_diff](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_diff) in seconds between dropoff_datetime and pickup_datetime - we'll call it `trip_duration` for this exercise
3. Compute the **continous** `p90` of `trip_duration` partitioning by year, month, pickup_location_id, and dropoff_location_id

For the Trips that **respectively** started from `Newark Airport`, `SoHo`, and `Yorkville East`, in November 2019, what are **dropoff_zones** with the 2nd longest p90 trip_duration ?

- LaGuardia Airport, Chinatown, Garment District
- LaGuardia Airport, Park Slope, Clinton East
- LaGuardia Airport, Saint Albans, Howard Beach
- LaGuardia Airport, Rosedale, Bath Beach
- LaGuardia Airport, Yorkville East, Greenpoint
#### Answer:  
- LaGuardia Airport, Chinatown, Garment District

```sql
WITH ranked_trips AS (
    SELECT 
        pz.zone AS pickup_zone,
        dz.zone AS dropoff_zone,
        t.travel_time_p90,
        ROW_NUMBER() OVER (PARTITION BY pz.zone ORDER BY t.travel_time_p90 DESC) AS trip_rank
    FROM advance-vector-447116-m5.trips_data_all.fct_fhv_monthly_zone_traveltime_p90 t
    JOIN advance-vector-447116-m5.trips_data_all.dim_zones pz ON t.pickup_locationid = pz.locationid
    JOIN advance-vector-447116-m5.trips_data_all.dim_zones dz ON t.dropoff_locationid = dz.locationid
    WHERE 
        t.year = 2019  AND t.month = 11
        AND pz.zone IN ('Newark Airport', 'SoHo', 'Yorkville East')
)

SELECT  pickup_zone, dropoff_zone, travel_time_p90
FROM ranked_trips
WHERE trip_rank = 2;
```
## Submitting the solutions
- Form for submitting: [https://courses.datatalks.club/de-zoomcamp-2025/homework/hw4](https://courses.datatalks.club/de-zoomcamp-2025/homework/hw4)
