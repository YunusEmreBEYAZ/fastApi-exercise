from pydantic import BaseModel,field_validator, Field
from datetime import date
from db.gender_enum import GenderEnum
from typing import List

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

class UserDisplay(BaseModel):
    username : str
    email : str
    first_name : str
    last_name :str
    date_of_birth: date
    gender: GenderEnum
    hotels: List[Hotel] = []
    class Config():     # automates type conversion
        orm_mode = True
    

class HotelBase(BaseModel):
    name: str
    city: str
    address: str
    email: str
    phone_number: str
    description: str
    available: bool
    user_id: int

class HotelDisplay(BaseModel):
    id: int
    name:str
    city: str
    address: str
    email: str
    phone_number: str
    rating: int
    owner: User
    class Config():
        from_attributes = True   

class RatingBase(BaseModel):
    #####
    rating_score: int = Field(..., ge=1, le=5)  # Ensure score is between 1 and 5
 