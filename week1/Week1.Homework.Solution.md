
## WSL and OS preparation
- Common tool setup
```bash
sudo apt install unzip
```
- Docker & Python installation  with step-by-step instructions
- PIP intallation 
```bash
pip install sqlalchemy psycopg2-binary 
pip install pandas
```
- Install CLI for Postgres 
```bash
pip install pgcli 
sudo apt install pgcli  
pip install keyrings.alt
```
- Install the classic Jupyter Notebook 
```bash
pip install notebook
```
  

## Question 1. Understanding docker first run
Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint `bash`.
What's the version of `pip` in the image?
### Answer: 
- 24.3.1

Command
```bash
docker run -it python:3.12.8 /bin/bash
pip --version
```
## Question 2.
Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?
### Answer: 
- postgres:5433


## Prepare Postgres and ingest data

```bash
docker pull postgres:13
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v /home/lan/DEZC/Projects/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
	
pgcli -h localhost -p 5432 -u root -d ny_taxi

cd /home/lan/DEZC/Projects/week1

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz	

gzip -d green_tripdata_2019-10.csv.gz 

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

python3 ingest_green_tripdata.py \
    --user=root \
    --password=root  \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_tripdata  
	
python3 ingest_zones.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones  
```

- Test queries
```sql
select * from public.green_tripdata limit 100;
select count(*) from public.green_tripdata;

select * from public.zones  limit 100;
select count(*) from public.zones
```


## Question 3. Trip Segmentation Count
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, **respectively**, happened:
1. Up to 1 mile
2. In between 1 (exclusive) and 3 miles (inclusive),
3. In between 3 (exclusive) and 7 miles (inclusive),
4. In between 7 (exclusive) and 10 miles (inclusive),
5. Over 10 miles
### Answer:  
- 104,802; 198,924; 109,603; 27,678; 35,189

Query
```sql
select
case
when trip_distance <=1 then '1.Up to 1 mile'
when trip_distance > 1 and trip_distance <= 3 then '2.In between 1 (exclusive) and 3 miles (inclusive)'
when trip_distance > 3 and trip_distance <= 7 then '3.In between 3 (exclusive) and 7 miles (inclusive)'
when trip_distance > 7 and trip_distance <= 10 then '4.In between 7 (exclusive) and 10 miles (inclusive)'
when trip_distance > 10 then '5.Over 10 miles'
end as range_
, count(*) as trips
from public.green_tripdata
where lpep_dropoff_datetime >= '20191001' and lpep_dropoff_datetime <'20191101'
group by case
when trip_distance <=1 then '1.Up to 1 mile'
when trip_distance > 1 and trip_distance <= 3 then '2.In between 1 (exclusive) and 3 miles (inclusive)'
when trip_distance > 3 and trip_distance <= 7 then '3.In between 3 (exclusive) and 7 miles (inclusive)'
when trip_distance > 7 and trip_distance <= 10 then '4.In between 7 (exclusive) and 10 miles (inclusive)'
when trip_distance > 10 then '5.Over 10 miles'
end
order by range_
```

## Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.
Tip: For every day, we only care about one single trip with the longest distance.

- 2019-10-11
- 2019-10-24
- 2019-10-26
- 2019-10-31
### Answer: 
- 2019-10-31

Query
```sql
SELECT
CAST(lpep_pickup_datetime AS DATE) as date_,
MAX(trip_distance) as trip_distance
from public.green_tripdata
GROUP BY 1
order by trip_distance desc
limit 1;
```

## Question 5. Three biggest pickup zones
Which were the top pickup locations with over 13,000 in `total_amount` (across all trips) for 2019-10-18?
Consider only `lpep_pickup_datetime` when filtering by date.
- East Harlem North, East Harlem South, Morningside Heights
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park

### Answer: 
- East Harlem North, East Harlem South, Morningside Heights

Query
```sql
SELECT z."Zone" , sum(d.total_amount) as total_amount
from public.green_tripdata d
inner join public.zones z on z."LocationID" = d."PULocationID"
where CAST(lpep_pickup_datetime as DATE) = '2019-10-18'
group by z."Zone"
having sum(d.total_amount) > 13000
```


## Question 6. Largest tip
For the passengers picked up in October 2019 in the zone name "East Harlem North" which was the drop off zone that had the largest tip?
Note: it's `tip` , not `trip`
We need the name of the zone, not the ID.

- Yorkville West
- JFK Airport
- East Harlem North
- East Harlem South
### Answer: 
- JFK Airport
Query
```sql
SELECT
zpu."Zone" AS Pickup_location
, zdo."Zone" AS Dropoff_location
, MAX(tip_amount) as tip_amount
from public.green_tripdata d
JOIN public.zones zpu ON d."PULocationID" = zpu."LocationID"
JOIN public.zones zdo ON d."DOLocationID" = zdo."LocationID"
where zpu."Zone" = 'East Harlem North'
GROUP BY 1, 2
ORDER BY tip_amount desc LIMIT 1;
```


## Terraform
In this section homework we'll prepare the environment by creating resources in GCP with Terraform.
In your VM on GCP/Laptop/GitHub Codespace install Terraform. Copy the files from the course repo [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.
Modify the files as necessary to create a GCP Bucket and Big Query Dataset.

	CGP - IAM- Service Accounts
	Create service account with 3 roles (BigQuery Admin,Storage Admin, Compute Admin)
	

## Question 7. Terraform Workflow
Which of the following sequences, **respectively**, describes the workflow for:
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:
- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm

### Answer: 
- terraform init, terraform apply -auto-approve, terraform destroy
## Submitting the solutions
- Form for submitting: [https://courses.datatalks.club/de-zoomcamp-2025/homework/hw1](https://courses.datatalks.club/de-zoomcamp-2025/homework/hw1)

