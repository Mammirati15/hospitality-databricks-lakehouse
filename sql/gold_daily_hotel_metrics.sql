-- gold_daily_hotel_metrics.sql
-- Aggregates booking-level data into daily hotel metrics

USE hospitality_dev;

CREATE OR REPLACE TABLE gold_daily_hotel_metrics AS
SELECT
    arrival_date,
    hotel,
    COUNT(*) AS total_bookings,
    SUM(is_canceled) AS canceled_bookings
FROM silver_hotel_bookings
GROUP BY arrival_date, hotel;