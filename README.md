# Hospitality Lakehouse (Databricks)

This project is a small lakehouse pipeline built in Databricks using the hotel booking demand dataset. The goal was to practice organizing raw data into Bronze, Silver, and Gold layers and then generate useful metrics from booking data.

The dataset contains hotel reservations for both city and resort hotels. It includes information such as arrival date, lead time, number of guests, ADR, and whether a booking was cancelled.

## Architecture

This project follows a simple medallion architecture in Databricks.

Raw CSV Dataset  
        ↓  
Bronze Layer  
bronze_hotel_bookings  

        ↓  
Silver Layer  
silver_hotel_bookings  

        ↓  
Gold Layer  
gold_daily_hotel_metrics  

        ↓  
Analytics / Queries

## Data Layers

### Bronze

**bronze_hotel_bookings**

The Bronze table stores the raw booking data loaded directly from the CSV dataset. This layer keeps the data close to the original source and acts as the starting point for the pipeline.

### Silver

**silver_hotel_bookings**

The Silver layer contains a cleaned and structured version of the booking data. Transformations include combining the separate arrival date columns into a single `arrival_date` field and preparing the data types for analysis.

### Gold

**gold_daily_hotel_metrics**

The Gold layer contains aggregated metrics used for analysis. These tables summarize the booking data at a daily level by hotel.

Examples of metrics in this layer include:

- total bookings  
- cancelled bookings  
- cancellation rate  
- ADR metrics  
- total nights booked  

## Example Analysis

One query looked at cancellation rates by day of the week.

Thursday had the highest cancellation rate at about **41%**, followed by Friday and Saturday.  
Tuesday had the lowest cancellation rate.

## Repository Structure

docs/
- data_model.md
- dataset.md
- metric_definitions.md
- project_plan.md
- scaling_plan.md
- silver_schema.md

sql/
- bronze_hotel_bookings.sql
- silver_hotel_bookings.sql
- gold_daily_hotel_metrics.sql

README.md

## Next Steps

Future improvements for this project include:

- automating the pipeline
- expanding the Gold layer with additional metrics
- connecting the tables to a dashboard