# Data Model Plan

## Bronze Layer
Table: bronze_hotel_bookings  
Grain: 1 row per raw booking record  
Purpose: Store raw ingested data exactly as received


## Silver Layer
Table: silver_hotel_bookings  
Grain: 1 row per cleaned booking  
Purpose:
- Standardized date column
- Derived total_nights column
- Derived booking_revenue column (adr * total_nights)
- Cleaned categorical values


## Gold Layer
Table: gold_daily_hotel_metrics  
Grain: 1 row per hotel per day  
Purpose:
- Total bookings
- Total revenue (realized + potential depending on cancellation handling)
- Cancellation rate
- Average ADR
- Average booking value
