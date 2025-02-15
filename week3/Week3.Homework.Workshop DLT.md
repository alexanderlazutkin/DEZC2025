- Course homework page: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/workshops/dlt/data_ingestion_workshop.md
- Due date: 17.02.2025 02:00 (local time)


# Workshop "Data Ingestion with dlt": Homework

## **Question 1: dlt Version**

### Answer:  
- dlt 1.6.1
#### Solution: 
``` 
!dlt --version
```


## **Question 2: Define & Run the Pipeline (NYC Taxi API)**

Use dlt to extract all pages of data from the API.
Steps:
1️⃣ Use the `@dlt.resource` decorator to define the API source.
2️⃣ Implement automatic pagination using dlt's built-in REST client.
3️⃣ Load the extracted data into DuckDB for querying.
- How many tables were created?
### Answer:  
- 4

#### Solution: 
```Python
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator

# Define the API resource for NYC taxi data
@dlt.resource(name="rides")   # <--- The name of the resource (will be used as the table name)

def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):    # <--- API endpoint for retrieving taxi ride data
        yield page   # <--- yield data to manage memory

  
pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_pipeline",
    destination="duckdb",
    dataset_name="ny_taxi_data"

)

# define new dlt pipeline
pipeline = dlt.pipeline(destination="duckdb")
```
```result
Pipeline dlt_colab_kernel_launcher load step completed in 2.20 seconds 1 load package(s) were loaded to destination duckdb and into dataset dlt_colab_kernel_launcher_dataset The duckdb destination used duckdb:////content/dlt_colab_kernel_launcher.duckdb location to store data Load package 1739627268.836814 is LOADED and contains no failed jobs
```

Load the data into DuckDB to test:
```Python
load_info = pipeline.run(ny_taxi)
print(load_info)
```
Start a connection to your database using native `duckdb` connection and look what tables were generated:
```Python
import duckdb
from google.colab import data_table
data_table.enable_dataframe_formatter()

# A database '<pipeline_name>.duckdb' was created in working directory so just connect to it
# Connect to the DuckDB database
conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")

# Set search path to the dataset
conn.sql(f"SET search_path = '{pipeline.dataset_name}'")

# Describe the dataset
conn.sql("DESCRIBE").df()
```
```Result
| _dlt_loads          |
| _dlt_pipeline_state |
| _dlt_version        |
| rides               |
```



## **Question 3: Explore the loaded data**
- What is the total number of records extracted?

### Answer:  
- 10000
#### Solution
Inspect the table `rides`:
```python
df = pipeline.dataset(dataset_type="default").rides.df()
df
```

## ## **Question 4: Trip Duration Analysis**
Run the SQL query below to calculate the average trip duration in minutes.
- What is the average trip duration?
### Answer:  
- 12.3049

#### Solution
```Python
with pipeline.sql_client() as client:
    res = client.execute_sql(
            """
            SELECT
            AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
            FROM rides;
            """
        )

    # Prints column values of the first row
    print(res)

```


## Submitting the solutions
Form for submitting:  https://courses.datatalks.club/de-zoomcamp-2025/homework/workshop1
