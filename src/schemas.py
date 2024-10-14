from pydantic import BaseModel,field_validator, Field
from datetime import date
from db.gender_enum import GenderEnum
from typing import List, Optional

class Hotel(BaseModel):
    id: int
    name: str
    address: str
    city: str

    class Config():
        from_attributes = True

class User(BaseModel):
    id: int
    username: str
    class Config():
        from_attributes = True 

class Booking(BaseModel):
    id: int
    checkin: date
    checkout: date
    class Config():
        from_attributes = True

class UserBase(BaseModel):
    username : str
    email : str
    password : str
    first_name : str
    last_name :str
    date_of_birth: date
    gender: GenderEnum
    phone_number: str
    @field_validator('gender', mode='before')
    def validate_gender(cls, value):
        if value not in GenderEnum.__members__.values():
            raise ValueError(f"Invalid gender '{value}'. Must be one of: {[e.value for e in GenderEnum]}")
        return value

class UserBaseAdmin(BaseModel):
    username : str
    email : str
    password : str
    first_name : str
    last_name :str
    date_of_birth: date
    gender: GenderEnum
    phone_number: str
    is_admin: bool
    @field_validator('gender', mode='before')
    def validate_gender(cls, value):
        if value not in GenderEnum.__members__.values():
            raise ValueError(f"Invalid gender '{value}'. Must be one of: {[e.value for e in GenderEnum]}")
        return value

class UserDisplay(BaseModel):
    id : int
    username : str
    email : str
    first_name : str
    last_name :str
    date_of_birth: date
    gender: GenderEnum
    profile_picture: Optional[str] = None  # Allow None as a valid value
    hotels: List[Hotel] = []
    class Config():     # automates type conversion
        orm_mode = True
    
class RatingBase(BaseModel):
    rating_score: int = Field(..., ge=1, le=5)  # Ensure score is between 1 and 5
    title: Optional[str] = None
    comment: Optional[str] = None
    class Config():
        from_attributes = True
class RatingDisplay(BaseModel):
    id: int
    rating_score: int
    rating_date: date
    title: Optional[str] = None
    comment: Optional[str] = None
    rated_hotel: Hotel
    rated_booking: Booking
    class Config():
        from_attributes = True

class HotelBase(BaseModel):
    name: str
    city: str
    address: str
    email: str
    phone_number: str
    description: str
    available: bool

class HotelDisplay(BaseModel):
    id: int
    name:str
    city: str
    address: str
    email: str
    phone_number: str
    description: str
    available: bool
    rating: str = "No ratings yet"  # Field for the average rating
    owner: User
    ratings: List[RatingBase] = []


    class Config():
        from_attributes = True   



 