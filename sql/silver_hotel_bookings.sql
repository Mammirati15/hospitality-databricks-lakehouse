USE hospitality_dev;

CREATE OR REPLACE TABLE silver_hotel_bookings AS
SELECT
    hotel,
    is_canceled,
    lead_time,

    TO_DATE(
        CONCAT(
            arrival_date_year,
            '-',
            CASE arrival_date_month
                WHEN 'January' THEN '01'
                WHEN 'February' THEN '02'
                WHEN 'March' THEN '03'
                WHEN 'April' THEN '04'
                WHEN 'May' THEN '05'
                WHEN 'June' THEN '06'
                WHEN 'July' THEN '07'
                WHEN 'August' THEN '08'
                WHEN 'September' THEN '09'
                WHEN 'October' THEN '10'
                WHEN 'November' THEN '11'
                WHEN 'December' THEN '12'
            END,
            '-',
            LPAD(arrival_date_day_of_month, 2, '0')
        )
    ) AS arrival_date,

    stays_in_weekend_nights,
    stays_in_week_nights,
    adults,
    children,
    babies,
    meal,
    country,
    market_segment

FROM bronze_hotel_bookings;


CREATE OR REPLACE TABLE silver_hotel_bookings AS
SELECT
    hotel,
    is_canceled,
    lead_time,
    adr,

    TO_DATE(
        CONCAT(
            arrival_date_year,
            '-',
            CASE arrival_date_month
                WHEN 'January' THEN '01'
                WHEN 'February' THEN '02'
                WHEN 'March' THEN '03'
                WHEN 'April' THEN '04'
                WHEN 'May' THEN '05'
                WHEN 'June' THEN '06'
                WHEN 'July' THEN '07'
                WHEN 'August' THEN '08'
                WHEN 'September' THEN '09'
                WHEN 'October' THEN '10'
                WHEN 'November' THEN '11'
                WHEN 'December' THEN '12'
            END,
            '-',
            LPAD(arrival_date_day_of_month, 2, '0')
        )
    ) AS arrival_date,

    stays_in_weekend_nights,
    stays_in_week_nights,
    adults,
    children,
    babies,
    meal,
    country,
    market_segment

FROM bronze_hotel_bookings;