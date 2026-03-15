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

CREATE OR REPLACE TABLE gold_daily_hotel_metrics AS
SELECT
  arrival_date,
  hotel,
  COUNT(*) AS total_bookings,
  SUM(is_canceled) AS canceled_bookings,
  ROUND(SUM(is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct,
  SUM(stays_in_weekend_nights + stays_in_week_nights) AS total_nights_booked,
  ROUND(AVG(adr), 2) AS average_adr,
  ROUND(SUM((stays_in_weekend_nights + stays_in_week_nights) * adr), 2) AS gross_booking_value,
  ROUND(
    SUM(
      CASE
        WHEN is_canceled = 0
        THEN (stays_in_weekend_nights + stays_in_week_nights) * adr
        ELSE 0
      END
    ), 2
  ) AS realized_booking_value
FROM silver_hotel_bookings
GROUP BY arrival_date, hotel;