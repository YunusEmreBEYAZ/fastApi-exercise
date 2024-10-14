from sqlalchemy.orm import Session
from db.models import DbRating, DbBooking, DbHotel
from schemas import RatingBase
from fastapi import HTTPException, status
from datetime import datetime
from sqlalchemy import func

def create_rating(db: Session, request: RatingBase, booking_id: int, current_user):
    booking = db.query(DbBooking).filter(DbBooking.id == booking_id).first()
    hotel = db.query(DbHotel).filter(DbHotel.id == booking.hotel_id).first()
    existing_rating = db.query(DbRating).filter(DbRating.user_id == current_user.id, DbRating.booking_id == booking_id).first()
    new_rating = DbRating(
        rating_score= request.rating_score,
        rating_date= datetime.now().date(),
        title= request.title,
        comment= request.comment,
        user_id= current_user.id,
        booking_id= booking_id,
        hotel_id=hotel.id
        )
    
    if not request.rating_score:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating score cannot be empty. Please choose between 1 and 5.")
    
    if not booking:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found with the {booking_id}.")
    
    if booking.client_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to rate this booking.")
    
    if existing_rating:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="You have already rated this booking.")
    
    if datetime.now().date() < booking.checkout:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="You can only rate a booking after the end date.")
    
    
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

def get_rating_by_id(db: Session , rating_id: int):
    rating = db.query(DbRating).filter(DbRating.id == rating_id).first()
    
    if not rating:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Rating with id {rating_id} not found.")
    
    return rating

def get_ratings_by_hotel_id(db: Session, hotel_id:int):
    ratings = db.query(DbRating).filter(DbRating.hotel_id == hotel_id).all()
    if not ratings:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"No ratings found for hotel with id {hotel_id}.")
    
    return ratings

def update_rating(db:Session, rating_id:int, request: RatingBase,current_user):
    rating = db.query(DbRating).filter(DbRating.id == rating_id).first()

    if not rating:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Rating with id {rating_id} not found.")

    booking = db.query(DbBooking).filter(DbBooking.id == rating.booking_id).first()
    if not booking:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Booking with id "
                                                                              f"{rating.booking_id} not found.")

    if not request.rating_score:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating score cannot be empty. Please choose between 1 and 5.")
    
    if rating.rating_date < booking.checkout:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="You can only rate a booking after the end date.")
    
    if booking.client_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to rate this booking.")
    
    

    rating.rating_score = request.rating_score
    rating.title = request.title
    rating.comment = request.comment
    db.commit()
    db.refresh(rating)
    return rating

def delete_rating(db:Session, rating_id:int, current_user):
    rating = db.query(DbRating).filter(DbRating.id == rating_id).first()

    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rating with the id {rating_id} not found.")

    booking = db.query(DbBooking).filter(DbBooking.id == rating.booking_id).first()

    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rating with the id "
                                                                          f"{rating.booking_id} not found.")

    if booking.client_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this rating.")
    
    db.delete(rating)
    db.commit()
    return f"Rating with id {rating_id} has been deleted."