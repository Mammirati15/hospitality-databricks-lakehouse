# Metric Definitions (v1)

## Dates
- arrival_date: the intended arrival date of the booking

## Revenue Metrics
We will track two revenue concepts:

1) Gross Booking Value (GBV)
- Definition: adr * total_nights for all bookings
- Includes canceled bookings
- Use case: demand / pipeline value

2) Realized Booking Value (RBV)
- Definition: adr * total_nights for non-canceled bookings only
- Excludes canceled bookings
- Use case: realized revenue proxy

## Cancellation Rate
- Definition: canceled_bookings / total_bookings
- canceled_bookings = count where is_canceled = 1

## ADR (Average Daily Rate)
- Track as:
  - avg_adr_all = average adr across all bookings
  - avg_adr_realized = average adr where is_canceled = 0

## Next build step
Implement Bronze → Silver in Databricks, then run Gold aggregation query to populate gold_daily_hotel_metrics.