import datetime
from schemas import Hotel
from pydantic import BaseModel, field_validator


class BookingDto(BaseModel):
    id: int
    rooms_amount: int
    guests_count: int
    checkin: datetime.date
    checkout: datetime.date
    additional_info: str
    client_username: str
    hotel: Hotel
    room_id: int
    room_guests_count: int


class BookingPostRequest(BaseModel):
    rooms_amount: int = 1
    guests_count: int = 1
    checkin: datetime.date
    checkout: datetime.date
    additional_info: str = ''
    hotel_id: int
    room_id: int

    @field_validator("rooms_amount", "guests_count")
    def check_negative(cls, val):
        if val <= 0:
            raise ValueError(f"Value {val} is incorrect. Should be positive")
        return val
