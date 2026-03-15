# Scaling Plan (Future Phases)

## Current v1 (MVP)
- Business process: room bookings only
- Silver: one wide booking-level table (silver_hotel_bookings)
- Gold: daily metrics at hotel + date grain (gold_daily_hotel_metrics)

## Future v2: Add new business processes
- Add restaurant POS sales (fact_fnb_sales)
- Add spa appointments/sales (fact_spa_sales)

## When we introduce dimensional modeling (star schema)
If multiple fact tables exist (bookings + F&B + spa), introduce shared dimensions:
- dim_hotel
- dim_date
- dim_channel
- dim_customer_segment (if available)

Reason: shared, consistent definitions across multiple transactional domains.
