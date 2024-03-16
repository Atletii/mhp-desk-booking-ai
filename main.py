import datetime
from enum import Enum

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
    half: str


class RoomRequest(BaseModel):
    name: str
    date: datetime.date
    timeframe: str


app = FastAPI()
app.add_exception_handler(Exception, custom_exception_handler)


@app.get("/predict/desk")
async def predict_desk_api(desk_request: DeskRequest):
    return predict_desk(desk_request.name, desk_request.date, desk_request.half)


@app.get("/predict/room")
async def predict_room_api(room_request: RoomRequest):
    return predict_room(room_request.name, room_request.date, room_request.timeframe)
