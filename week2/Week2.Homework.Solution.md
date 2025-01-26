- Course homework page: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/02-workflow-orchestration/homework.md
- Course materials:
	- https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration
	- Check out the GitHub Repository here: https://go.kestra.io/de-zoomcamp
- Due date: 4 февраль 2025 02:00 (local time)

# Prepare environment on WSL
### Setup Kestra & PostgreSQL
Run containers 
```bash
cd ~/02-workflow-orchestration
docker compose up -d  #Kestra
cd ~/02-workflow-orchestration\postgres
docker compose up -d # PostgreSQL
```
select version();
PostgreSQL 17.2 (Debian 17.2-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit


Importing flows programmatically using Kestra's API with following commands:
```shell
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/01_getting_started_data_pipeline.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/02_postgres_taxi.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/02_postgres_taxi_scheduled.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/03_postgres_dbt.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/04_gcp_kv.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/05_gcp_setup.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/06_gcp_taxi.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/06_gcp_taxi_scheduled.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/07_gcp_dbt.yaml
```
### Working with local DB
- Load Taxi Data to Postgres
- Backfilling the the data for the year 2021 (2021-01-01 - 2021-07-31)
	- Run the flow in Kestra [zoomcamp.02_postgres_taxi_scheduled](http://localhost:8080/ui/flows/edit/zoomcamp/02_postgres_taxi_scheduled) and setup backfilling period
### Working with GCP
- Configure service account and permissions (Storage and BQ Admins)
- Configure and run Kestra flow 04_gcp_kv.yaml
- Setup GCP bucket and dataset with Kestra: run flow 05_gcp_setup.yaml
- Run data loading into BQ with backfilling as trigger option for the green & yellow taxi datasets: 06_gcp_taxi_scheduled.yaml


## Question 1.
Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?
- 128.3 MB
- 134.5 MB
- 364.7 MB
- 692.6 MB
### Answer:  
- 128.3 MB
#### Solution: 
- Setup for the flow task <purge_files> `disabled: true` 
- Run and select execution in Kestra UI: Executions - Tasks (extract) - Outputs (outputFiles) - yellow_tripdata_2020-12.csv - Debug outputs - Getting info about file


## Question 2. 
What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?
- {{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv
- green_tripdata_2020-04.csv
- green_tripdata_04_2020.csv
- green_tripdata_2020.csv
### Answer:  
- green_tripdata_2020-04.csv

## Question 3. 
How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?
- 13,537,299
- 24,648,499
- 18,324,219
- 29,430,127
### Answer:  
- 24,648,499

#### Solution
```sql
SELECT  COUNT(*)
FROM `advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata`
WHERE filename like 'yellow_tripdata_2020%'

```
## Question 4.
How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?
- 5,327,301
- 936,199
- 1,734,051
- 1,342,034
### Answer:  
- 1,734,051
#### Solution
```sql
SELECT  COUNT(*)
FROM `advance-vector-447116-m5.dezc2025demo97546.green_tripdata`
WHERE filename like 'green_tripdata_2020%'
```

## Question 5. 
How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?
- 1,428,092
- 706,911
- 1,925,152
- 2,561,031
### Answer:  
- 1,925,152

#### Solution
```sql
SELECT  COUNT(*)
FROM `advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata`
WHERE filename = 'yellow_tripdata_2021-03.csv'
```

## Question 6. 
How would you configure the timezone to New York in a Schedule trigger?
- Add a `timezone` property set to `EST` in the `Schedule` trigger configuration
- Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration
- Add a `timezone` property set to `UTC-5` in the `Schedule` trigger configuration
- Add a `location` property set to `New_York` in the `Schedule` trigger configuration
### Answer:  
- Add a `timezone` property set to `UTC-5` in the `Schedule` trigger configuration

#### Solution
- Add timezone property for schedule https://kestra.io/plugins/core/triggers/io.kestra.plugin.core.trigger.schedule#timezone into yaml

## Submitting the solutions
- Form for submitting: [https://courses.datatalks.club/de-zoomcamp-2025/homework/hw2](https://courses.datatalks.club/de-zoomcamp-2025/homework/hw2)
