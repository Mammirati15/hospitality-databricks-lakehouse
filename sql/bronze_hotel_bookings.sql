-- bronze_hotel_bookings.sql
-- Raw ingestion layer for hotel booking dataset

USE hospitality_dev;

-- In production this would read from cloud storage (S3 / ADLS / GCS)
-- For this project the CSV was uploaded via the Databricks UI

CREATE OR REPLACE TABLE bronze_hotel_bookings AS
SELECT *
FROM read_files(
  '/Volumes/hospitality_dev/raw/hotel_bookings.csv',
  format => 'csv',
  header => true
);