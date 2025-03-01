- Course homework page: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/05-batch/homework.md
- Course materials: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/README.md
- Due date: 07.03.2025 02:00 (local time)



## Module 5 Homework 

In this homework we'll put what we learned about Spark in practice.
For this homework we will be using the Yellow 2024-10 data from the official website:
```shell
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-10.parquet
```
Install Jupyter Notebooks 
sudo apt install jupyter-core

### Question 1: Install Spark and PySpark
- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.
What's the output?
#### Answer:  
- '3.3.2' 

#### Solution
- Install Spark on Linux with existing guide https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/setup/linux.md
- Run PySpark https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/setup/pyspark.md
- Install Jupyter Notebooks https://code.adonline.id.au/jupyter-notebook-in-windows-subsystem-for-linux-wsl/
- Open and run homework notebook till 'spark.version'  https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/code/homework.ipynb
- See detail in [homework.ipynb](https://github.com/alexanderlazutkin/DEZC2025/blob/main/week5/homework.ipynb) file

### Question 2: Yellow October 2024
Read the October 2024 Yellow into a Spark Dataframe.
Repartition the Dataframe to 4 partitions and save it to parquet.
What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 6MB
- 25MB
- 75MB
- 100MB
#### Answer:  
- 25MB
#### Solution
- See detail in [homework.ipynb](https://github.com/alexanderlazutkin/DEZC2025/blob/main/week5/homework.ipynb) file

### Question 3: Count records
How many taxi trips were there on the 15th of October?
Consider only trips that started on the 15th of October.

- 85,567
- 105,567
- 125,567
- 145,567
#### Answer:  
- 125,567
#### Solution
- See detail in homework.ipynb file

### Question 4: Longest trip
What is the length of the longest trip in the dataset in hours?
- 122
- 142
- 162
- 182
#### Answer:  
- 162
#### Solution
- See detail in [homework.ipynb](https://github.com/alexanderlazutkin/DEZC2025/blob/main/week5/homework.ipynb) file

### Question 5: User Interface
Spark’s User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040
- 8080
#### Answer:  
- 4040
#### Solution
- https://spark.apache.org/docs/latest/monitoring.html#:~:text=Every%20SparkContext%20launches%20a%20Web,useful%20information%20about%20the%20application.

### Question 6: Least frequent pickup location zone
Load the zone lookup data into a temp view in Spark:
```shell
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```
Using the zone lookup data and the Yellow October 2024 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay

#### Answer:  
- Governor's Island/Ellis Island/Liberty Island
#### Solution
- See detail in [homework.ipynb](https://github.com/alexanderlazutkin/DEZC2025/blob/main/week5/homework.ipynb) file
## Submitting the solutions
- Form for submitting: [https://courses.datatalks.club/de-zoomcamp-2025/homework/hw5](https://courses.datatalks.club/de-zoomcamp-2025/homework/hw5)
