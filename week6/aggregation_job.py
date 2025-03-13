from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, DataTypes, TableEnvironment, StreamTableEnvironment
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common.time import Duration

def create_green_trips_source(t_env):
    table_name = "green_trips_source"
    pattern = "yyyy-MM-dd HH:mm:ss"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            passenger_count INTEGER,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
			event_watermark AS TO_TIMESTAMP(lpep_pickup_datetime, '{pattern}'),
            WATERMARK FOR event_watermark AS event_watermark - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda-1:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json',
	        'json.fail-on-missing-field' = 'false', 
            'json.ignore-parse-errors' = 'true'     
        );
        """
    t_env.execute_sql(source_ddl)
    return table_name

def create_green_trips_sink(t_env):
    table_name = 'aggregated_trips'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,
            DOLocationID INTEGER,
            session_start TIMESTAMP(3),
            session_end TIMESTAMP(3),
            num_trips BIGINT,
			session_duration BIGINT,
            PRIMARY KEY (PULocationID, DOLocationID, session_start) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
        """
    t_env.execute_sql(sink_ddl)
    return table_name

def log_aggregation():
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(60 * 1000)
    env.set_parallelism(1)


    # Set up the table environment
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)
	
	

    try:
        # Create Kafka table for green trips
        source_table = create_green_trips_source(t_env)
        aggregated_table = create_green_trips_sink(t_env)

        t_env.execute_sql(f"""
        INSERT INTO {aggregated_table}
        SELECT
            PULocationID,
            DOLocationID,
            SESSION_START(event_watermark, INTERVAL '5' MINUTE) AS session_start,
            SESSION_END(event_watermark, INTERVAL '5' MINUTE) AS session_end,
            COUNT(*) AS num_trips,
			TIMESTAMPDIFF(SECOND, SESSION_START(event_watermark, INTERVAL '5' MINUTE), SESSION_END(event_watermark, INTERVAL '5' MINUTE)) as session_duration
        FROM {source_table} 
        GROUP BY PULocationID, DOLocationID, SESSION(event_watermark, INTERVAL '5' MINUTE)
		ORDER BY session_duration DESC LIMIT 1;
        """).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))

if __name__ == '__main__':
    log_aggregation()