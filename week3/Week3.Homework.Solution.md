- Course homework page: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/02-workflow-orchestration/homework.md
- Course materials:
	- https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse
	- Check out the GitHub Repository here: https://go.kestra.io/de-zoomcamp
- Due date: 11.02.2025 02:00 (local time)

**Important Note:**
	For this homework we will be using the Yellow Taxi Trip Records for **January 2024 - June 2024 NOT the entire year of data** Parquet Files from the New York City Taxi Data found here:  
	[https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)  	If you are using orchestration such as Kestra, Mage, Airflow or Prefect etc. do not load the data into Big Query using the orchestrator.  Stop with loading the files into a bucket.  
	**Load Script:** You can manually download the parquet files and upload them to your GCS Bucket or you can use the linked script [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/03-data-warehouse/load_yellow_taxi_data.py):  
	You will simply need to generate a Service Account with GCS Admin Priveleges or be authenticated with the Google SDK and update the bucket name in the script to the name of your bucket  
	Nothing is fool proof so make sure that all 6 files show in your GCS Bucket before begining.  
	NOTE: You will need to use the PARQUET option files when creating an External Table

# Prepare environment on WSL

### Setup GCP from previous homework
- Configure service account and permissions (Storage and BQ Admins)
- Setup GCP bucket and dataset with Kestra: run flow 05_gcp_setup.yaml
- **BIG QUERY SETUP:**  
	Create an external table using the Yellow Taxi Trip Records.  
	Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table).
```bash
sudo pip3 install google-cloud-storage
cd ~/DEZC/Projects/week3
python3 load_yellow_taxi_data.py
```
#### Create external table referring to gcs path:
```sql
CREATE OR REPLACE EXTERNAL TABLE `advance-vector-447116-m5.dezc2025demo97546.ext_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezc2025demo97546/yellow_tripdata_2024*.parquet']
);
```
#### Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table)
```sql
CREATE OR REPLACE TABLE advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_regular AS
SELECT * FROM advance-vector-447116-m5.dezc2025demo97546.ext_yellow_tripdata_2024;
```



## Question 1.
Question 1: What is count of records for the 2024 Yellow Taxi Data?
- 65,623
- 840,402
- 20,332,093
- 85,431,289
### Answer:  
- 20,332,093
#### Solution: 
```sql
SELECT COUNT(*)
FROM advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_regular;
```


## Question 2. 
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.  What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?
- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 155.12 MB for the Materialized Table
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table
### Answer:  
- 0 MB for the External Table and 155.12 MB for the Materialized Table

#### Solution: 
```sql
SELECT COUNT(DISTINCT(PULocationID))
FROM advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_regular;
--This query will process 155.12 MB when run
SELECT COUNT(DISTINCT(PULocationID))
FROM advance-vector-447116-m5.dezc2025demo97546.ext_yellow_tripdata_2024;
--This query will process 0 B when run
```
## Question 3. 
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed
### Answer:  
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

#### Solution
```sql
SELECT PULocationID
FROM advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_regular;
--This query will process 155.12 MB when run
SELECT PULocationID, DOLocationID
FROM advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_regular;
--This query will process 310.24 MB when run
```
## Question 4.
How many records have a fare_amount of 0?
- 128,210
- 546,578
- 20,188,016
- 8,333
### Answer:  
- 8,333
#### Solution
```sql
SELECT COUNT(fare_amount)
FROM advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_regular
WHERE fare_amount = 0 
```

## Question 5. 
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
- Partition by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID
### Answer:  
- Partition by tpep_dropoff_datetime and Cluster on VendorID

#### Solution
```sql
CREATE OR REPLACE TABLE advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS 
SELECT * FROM advance-vector-447116-m5.dezc2025demo97546.ext_yellow_tripdata_2024;
```

## Question 6. 
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?  
Choose the answer which most closely matches.  
- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table
### Answer:  
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

#### Solution
```sql
SELECT DISTINCT(VendorID) 
FROM advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_regular
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
--This query will process 310.24 MB when run
SELECT DISTINCT(VendorID) 
FROM advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_partitioned_clustered
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
--This query will process 26.84 MB when run
```

## Question 7. 
Where is the data stored in the External Table you created?
- Big Query
- Container Registry
- GCP Bucket
- Big Table
### Answer:  
- GCP Bucket

#### Solution
- https://cloud.google.com/bigquery/docs/external-data-cloud-storage#sql

## Question 8. 
It is best practice in Big Query to always cluster your data:
- True
- False
### Answer:  
- False

#### Solution
- https://cloud.google.com/bigquery/docs/clustered-tables#when_to_use_clustering
- https://cloud.google.com/bigquery/docs/querying-clustered-tables

## Question 9. 
No Points: Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
### Answer:  
- This query will process 0 B when run. BigQuery does not scan actual data and getting answer from metadata tables.

#### Solution
```sql
SELECT count(*)
FROM advance-vector-447116-m5.dezc2025demo97546.yellow_tripdata_2024_regular
--This query will process 0 B when run.
```

## Submitting the solutions
Form for submitting: [https://courses.datatalks.club/de-zoomcamp-2025/homework/hw3](https://courses.datatalks.club/de-zoomcamp-2025/homework/hw3)
