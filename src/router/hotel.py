from typing import List
from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_hotel
from schemas import HotelBase, HotelDisplay



router = APIRouter(
    prefix= "/hotel",
    tags= ["hotel"]
)

# create hotel
@router.post("/", response_model=HotelDisplay)
def create_hotel(request: HotelBase, db:Session = Depends(get_db)):
    return db_hotel.create_hotel(db,request)

# update hotel
@router.put("/update/{id}", response_model=HotelDisplay)
def update_hotel(id:int, request: HotelBase, db:Session =Depends(get_db)):
    return db_hotel.update_hotel(db,id,request)


# get specific hotel
@router.get("/hotels/{id}", response_model = HotelDisplay)
def get_hotel(id:int = None, db:Session = Depends(get_db)):
    return db_hotel.get_hotel(db,id)

# get hotels by city
@router.get("/city/{city_name}", response_model=List[HotelDisplay])
def get_hotel_by_city(city_name:str, db:Session = Depends(get_db)):
    return db_hotel.get_hotel_by_city(db,city_name)

# delete hotel
@router.delete("/delete/{id}")
def delete_hotel(id:int = None, db:Session = Depends(get_db)):
    return db_hotel.delete_hotel(db,id)