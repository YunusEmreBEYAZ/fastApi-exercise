from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_rating
from schemas import RatingBase, RatingDisplay, UserBase
from auth.oauth2 import get_current_user
from typing import List


router = APIRouter(
    prefix= "/ratings",
    tags= ["ratings"]
)

@router.post("/rate/{booking_id}", response_model= RatingDisplay, summary="Rate a hotel after a booking", description="Rate a hotel after a booking with the provided details")
def create_rating(request:RatingBase, booking_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_rating.create_rating(db, request, booking_id,current_user)

@router.get("/{rating_id}", response_model = RatingDisplay, summary="Get a rating with id", description="Get a rating with the provided id")
def get_rating_by_id(rating_id: int, db: Session = Depends(get_db)):
    return db_rating.get_rating_by_id(db, rating_id)

@router.get("/", response_model= List[RatingDisplay], summary="Get all ratings", description="Get all ratings of the hotel from the database with the provided hotel id")
def get_ratings_by_hotel_id(hotel_id: int, db: Session = Depends(get_db)):
    return db_rating.get_ratings_by_hotel_id(db, hotel_id)

@router.put("/update/{rating_id}", response_model= RatingDisplay, summary="Update a rating", description="Update a rating with the provided details")
def update_rating(request:RatingBase, rating_id: int, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    return db_rating.update_rating(db,rating_id,request,current_user)

@router.delete("/delete/{rating_id}", summary="Delete a rating", description="Delete a rating with the provided id")
def delete_rating(db: Session = Depends(get_db), rating_id: int = None, current_user: UserBase = Depends(get_current_user)):
    return db_rating.delete_rating(db, rating_id, current_user)