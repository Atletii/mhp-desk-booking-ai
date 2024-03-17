# Room and Desk Occupancy Prediction Microservice

## Overview
This microservice offers an API for predicting the occupancy of desks and rooms based on historical usage data. It utilizes machine learning models to forecast occupancy rates for specified dates and times, enabling efficient space management and planning.

## Features
- Desk Occupancy Prediction: Predicts the average occupancy rate of a desk for a given week.
- Room Occupancy Prediction: Predicts the average occupancy rate of a room at certain time intervals (9-11, 11-13, 13-15, 15-17)

Flexible Timeframes: Supports predictions for specific parts of the day, allowing for detailed scheduling and planning.

# Installation
## Prerequisites
- Python 3.8+
- Pandas
- FastAPI
- Uvicorn (for running the FastAPI app)
- Pydantic

# Usage
## Running the Server
Start the FastAPI server by running:
`uvicorn main:app --reload`

## API Endpoints
The microservice provides two main endpoints for predicting availability:

* POST /predict/desk 
* POST /predict/room
