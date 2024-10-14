from typing import List
from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_hotel
from schemas import HotelBase, HotelDisplay, UserBase
from auth.oauth2 import get_current_user



router = APIRouter(
    prefix= "/hotels",
    tags= ["hotels"]
)

# create hotel
@router.post("/", response_model=HotelDisplay, summary="Create a new hotel", description="Create a new hotel with the provided details")
def create_hotel(request: HotelBase, db:Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    return db_hotel.create_hotel(db,request,current_user)

# update hotel
@router.put("/update/{id}", response_model=HotelDisplay, summary="Update a hotel", description="Update a hotel with the provided details")
def update_hotel(id:int, request: HotelBase, db:Session =Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    return db_hotel.update_hotel(db,id,request,current_user)


# get specific hotel
@router.get("/hotel", response_model = HotelDisplay, summary="Get a hotel with id", description="Get a hotel with the provided id")
def get_hotel(id:int = None, db:Session = Depends(get_db)):
    return db_hotel.get_hotel(db,id)


# get all hotels
@router.get("/", response_model=List[HotelDisplay], summary="Get all hotels", description="Get all hotels from the database")
def get_all_hotels(db:Session = Depends(get_db)):
    return db_hotel.get_all_hotels(db)

# delete hotel
@router.delete("/delete/{id}", summary="Delete a hotel", description="Delete a hotel with the provided id")
def delete_hotel(id:int = None, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_hotel.delete_hotel(db,id,current_user)