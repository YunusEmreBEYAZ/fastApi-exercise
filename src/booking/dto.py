import datetime
from schemas import Hotel
from db.booking_status_enum import BookingStatusEnum
from pydantic import BaseModel, field_validator


class BookingDto(BaseModel):
    id: int
    room_amount: int
    guests_count: int
    date_start: datetime.date
    date_end: datetime.date
    status: BookingStatusEnum
    additional_info: str
    client_username: str
    hotel: Hotel


class BookingPostRequest(BaseModel):
    room_amount: int
    guests_count: int
    date_start: datetime.date
    date_end: datetime.date
    additional_info: str
    client_username: str
    hotel_id: int

    @field_validator("room_amount", "guests_count")
    def check_negative(cls, val):
        if val <= 0:
            raise ValueError(f"Value {val} is incorrect. Should be positive")
        return val
