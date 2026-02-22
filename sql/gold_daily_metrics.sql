-- gold_daily_metrics.sql
-- Aggregates booking-level silver_hotel_bookings into hotel+date daily metrics (Gold)

WITH bookings AS (
  SELECT
    hotel,
    CAST(arrival_date AS DATE) AS arrival_date,
    is_canceled,
    adr,
    total_nights,
    booking_value
  FROM silver_hotel_bookings
),

daily AS (
  SELECT
    hotel,
    arrival_date,
    COUNT(*) AS total_bookings,
    SUM(CASE WHEN is_canceled = 1 THEN 1 ELSE 0 END) AS canceled_bookings,
    SUM(booking_value) AS gross_booking_value, -- GBV: includes canceled
    SUM(CASE WHEN is_canceled = 0 THEN booking_value ELSE 0 END) AS realized_booking_value, -- RBV: excludes canceled
    AVG(adr) AS avg_adr_all,
    AVG(CASE WHEN is_canceled = 0 THEN adr ELSE NULL END) AS avg_adr_realized,
    SUM(total_nights) AS total_nights_booked
  FROM bookings
  GROUP BY hotel, arrival_date
)

SELECT
  hotel,
  arrival_date,
  total_bookings,
  canceled_bookings,
  CASE WHEN total_bookings = 0 THEN 0 ELSE canceled_bookings::DOUBLE / total_bookings END AS cancellation_rate,
  gross_booking_value,
  realized_booking_value,
  avg_adr_all,
  avg_adr_realized,
  total_nights_booked,
  CASE WHEN total_nights_booked = 0 THEN 0 ELSE realized_booking_value / total_nights_booked END AS realized_revenue_per_night
FROM daily
ORDER BY hotel, arrival_date;