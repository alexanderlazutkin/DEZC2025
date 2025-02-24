SELECT
    -- Identifiers
    to_hex(md5(cast(coalesce(cast(dispatching_base_num as string), '_surrogate_key_null_') || '-' || coalesce(cast(pickup_datetime as string), '_surrogate_key_null_') as string))) AS tripid,
    dispatching_base_num,

    -- Timestamps
    SAFE_CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    SAFE_CAST(drop_off_datetime AS TIMESTAMP) AS dropoff_datetime,

    -- Date dimensions (fixed)
    EXTRACT(YEAR FROM SAFE_CAST(pickup_datetime AS TIMESTAMP)) AS year,
    EXTRACT(MONTH FROM SAFE_CAST(pickup_datetime AS TIMESTAMP)) AS month,

    -- Location Info
    SAFE_CAST(pu_location_id AS INT64) AS pickup_locationid,
    SAFE_CAST(do_location_id AS INT64) AS dropoff_locationid,

    -- Additional Fields
    SAFE_CAST(sr_flag AS INT64) AS sr_flag,
    affiliated_base_number

FROM `advance-vector-447116-m5`.`trips_data_all`.`fhv_trips`
WHERE dispatching_base_num IS NOT NULL
