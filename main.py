import datetime
from enum import Enum

import pandas as pd
from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from model_predictor import predict_desk, predict_room


async def custom_exception_handler(_, exc):
    detail = f"Exception: {str(exc)}"
    return JSONResponse(content={"detail": detail}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeskRequest(BaseModel):
    name: str
    date: datetime.date


class RoomRequest(BaseModel):
    name: str
    date: datetime.date


app = FastAPI()
app.add_exception_handler(Exception, custom_exception_handler)


def predict_desk_week_average(desk, selected_date):
    # Convert selected_date to a datetime object
    selected_date = pd.to_datetime(selected_date)

    # Determine the start and end of the week for the selected_date
    start_of_week = selected_date - pd.Timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + pd.Timedelta(days=4)

    # Initialize a list to hold the average predictions for each day
    week_averages = []

    # Iterate over each day of the week
    for single_date in pd.date_range(start=start_of_week, end=end_of_week):
        # Format single_date to match the expected date format in predict_desk
        formatted_date = single_date.strftime('%d/%m/%Y')

        # Calculate predictions for both halves of the day
        try:
            first_half_prediction = predict_desk(desk, formatted_date, 'first')
            second_half_prediction = predict_desk(desk, formatted_date, 'second')

            # Calculate the average prediction for the day
            daily_average = (first_half_prediction + second_half_prediction) / 2

            # Append the average to the list
            week_averages.append(daily_average)
        except Exception as e:
            print(f"Error processing {formatted_date}: {e}")
            week_averages.append(None)

    # Return the list of averages for the week
    return week_averages


def predict_room_week_average(room, selected_date):
    # Convert selected_date to a datetime object
    selected_date = pd.to_datetime(selected_date)

    # Determine the start and end of the week for the selected_date
    start_of_week = selected_date - pd.Timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + pd.Timedelta(days=4)

    # Define the timeframes to iterate over
    timeframes = ['nineToEleven', 'elevenToOne', 'oneToThree', 'threeToFive']

    # Initialize a list to hold the average predictions for each day
    week_averages = []

    # Iterate over each day of the week
    for single_date in pd.date_range(start=start_of_week, end=end_of_week):
        # Format single_date to match the expected date format in predict_room
        formatted_date = single_date.strftime('%d/%m/%Y')
        daily_predictions = []

        # Iterate over each timeframe and calculate predictions
        for timeframe in timeframes:
            try:
                prediction = predict_room(room, formatted_date, timeframe)
                daily_predictions.append(prediction)
            except Exception as e:
                print(f"Error processing {formatted_date} during {timeframe}: {e}")
                # Optionally, handle specific errors (e.g., append None or continue)

        # Calculate the daily average if there are any successful predictions
        if daily_predictions:
            daily_average = sum(daily_predictions) / len(daily_predictions)
        else:
            daily_average = None

        # Append the daily average to the week averages list
        week_averages.append(daily_average)

    # Return the list of averages for the week
    return week_averages


@app.get("/predict/desk")
async def predict_desk_api(desk_request: DeskRequest):
    return predict_desk_week_average(desk_request.name, desk_request.date)


@app.get("/predict/room")
async def predict_room_api(room_request: RoomRequest):
    return predict_room_week_average(room_request.name, room_request.date)
