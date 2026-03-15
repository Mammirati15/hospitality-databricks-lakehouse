# Silver Table Schema (Planned)

Table: silver_hotel_bookings  
Grain: 1 row per booking record (cleaned)

## Required Columns
- hotel (string)
- is_canceled (int/bool)

## Date Columns
- arrival_date (date)  ← derived from year/month/day fields

## Stay & Guest Columns
- stays_in_weekend_nights (int)
- stays_in_week_nights (int)
- total_nights (int)  ← weekend + week
- adults (int)
- children (int)
- babies (int)

## Pricing / Value Columns
- adr (float)  ← average daily rate
- booking_value (float)  ← adr * total_nights

## Segmentation Columns
- market_segment (string)
- distribution_channel (string)

## Notes
- Silver is where we standardize types, clean nulls, and create derived fields.
- Gold will aggregate from Silver (hotel + date grain).
