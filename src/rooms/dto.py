import datetime
from schemas import Hotel
from pydantic import BaseModel, field_validator


class RoomDto(BaseModel):
    id: int
    rooms_amount: int
    guests_count: int
    status: bool
    hotel: Hotel


class RoomRequest(BaseModel):
    rooms_amount: int
    guests_count: int
    status: bool

    @field_validator("rooms_amount", "guests_count")
    def check_positive(cls, val):
        if val <= 0:
            raise ValueError(f"Value {val} is incorrect. Should be positive")
        return val
