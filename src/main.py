import booking.controller
from fastapi import FastAPI, Request, status
from router import user_get, user_post, hotel,file, excel_file, dependencies
from db import models
from db.database import engine
from exceptions import InconsistentDatesException, DatesException
from booking.exceptions import BookingStatusException, BookingNotFoundException
from fastapi.responses import JSONResponse
from booking.exceptions import BookingStatusException, BookingNotFoundException, BookingException
from fastapi.responses import JSONResponse
from auth import authentication
from fastapi.staticfiles import StaticFiles
import time

app = FastAPI()
app.include_router(dependencies.router)
app.include_router(user_get.router)
app.include_router(file.router)
app.include_router(excel_file.router)
app.include_router(user_post.router)
app.include_router(hotel.router)
app.include_router(booking.controller.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(engine)

# to make the images folder accessible from the browser
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/")
def read_root():
    return "Hello PyBooking!"

@app.middleware("http")
async def get_duration(request: Request, next_call):
    start_time = time.time()
    response = await next_call(request)
    duration = time.time() - start_time
    response.headers["Duration"] = str(duration)
    return response


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
        status_code=status. HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': exc.message}
    )


@app.exception_handler(InconsistentDatesException)
def inconsistent_dates_exception_handler(request: Request, exc: InconsistentDatesException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': exc.message}
    )


@app.exception_handler(DatesException)
def dates_exception_handler(request: Request, exc: InconsistentDatesException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': exc.message}
    )
