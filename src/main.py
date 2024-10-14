import booking.controller, rooms.controller
from fastapi import FastAPI, Request, status
from router import user_get, user_post, hotel, rating
from db import models
from db.database import engine, SessionLocal
from exceptions import InconsistentDatesException, DatesException
from booking.exceptions import BookingStatusException, BookingNotFoundException, BookingException
from fastapi.responses import JSONResponse
from auth import authentication
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from db.models import DbUser
from db.hash import Hash
from contextlib import asynccontextmanager
import datetime
import data


@asynccontextmanager
async def lifespan(app: FastAPI):
    data.create_admin_user()
    data.create_dummy_users()
    data.create_hotel()
    data.create_dummy_bookings()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(user_get.router)
app.include_router(user_post.router)
app.include_router(hotel.router)
app.include_router(booking.controller.router)
app.include_router(authentication.router)
app.include_router(rating.router)
app.include_router(rooms.controller.router)


models.Base.metadata.create_all(engine)

@app.get("/")
def read_root():
    return "Hello PyBooking!"

app.mount('/files', StaticFiles(directory="files"), name='files')


@app.exception_handler(BookingStatusException)
def booking_status_exception_handler(request: Request, exc: BookingStatusException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': exc.message}
    )

@app.exception_handler(BookingNotFoundException)
def booking_not_found_exception_handler(request: Request, exc: BookingNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'detail': exc.message}
    )

@app.exception_handler(BookingException)
def booking_exception_handler(request: Request, exc: BookingException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': exc.message}
    )

@app.exception_handler(InconsistentDatesException)
def inconsistent_dates_exception_handler(request: Request, exc: InconsistentDatesException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': exc.message}
    )

@app.exception_handler(DatesException)
def dates_exception_handler(request: Request, exc: DatesException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': exc.message}
    )
