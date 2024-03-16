import datetime
from enum import Enum

from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


async def custom_exception_handler(_, exc):
    detail = f"Exception: {str(exc)}"
    return JSONResponse(content={"detail": detail}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeskRequest(BaseModel):
    name: str
    date: datetime.date
    half: Enum('half', ['first', 'second'])


class RoomRequest(BaseModel):
    name: str
    date: datetime.date
    timeframe: Enum('timeframe', ['nineToEleven', 'elevenToOne', 'oneToThree', 'threeToFive'])


app = FastAPI()
app.add_exception_handler(Exception, custom_exception_handler)


@app.get("/predict/desk")
async def predict_desk(desk_request: DeskRequest):
    pass


@app.get("/predict/room")
async def predict_room(
        text: str,
        embedding_group_id: str,
        offset: int,
        limit: int
):
    pass
