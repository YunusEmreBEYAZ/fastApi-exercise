from sqlalchemy.orm import Session
from db.models import DbHotel, DbRating
from schemas import HotelBase, HotelDisplay, RatingBase
from fastapi import HTTPException, status

def calculate_average_rating(hotel_ratings):
    if hotel_ratings:
        total_score = sum([rating.rating_score for rating in hotel_ratings])
        average_rating = total_score / len(hotel_ratings)
        return f"{str(round(average_rating, 1))}/5"
    return "No ratings yet"


def hotel_to_display(hotel):
    rating_str = calculate_average_rating(hotel.ratings)
    return HotelDisplay(
        id=hotel.id,
        name=hotel.name,
        city=hotel.city,
        address=hotel.address,
        email=hotel.email,
        phone_number=hotel.phone_number,
        rating=rating_str,
        description=hotel.description,
        available=hotel.available,
        owner=hotel.owner,
        ratings=hotel.ratings
    )

def create_hotel(db: Session, request: HotelBase, current_user):
    new_hotel = DbHotel(
        name= request.name.lower(),
        city= request.city.lower(),
        address= request.address,
        email= request.email,
        phone_number= request.phone_number,
        description= request.description,
        user_id= current_user.id
        )
    
    if not request.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hotel name cannot be empty."
        )
    
    if not request.city.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City name cannot be empty."
        )
    
    if not request.address.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address cannot be empty."
        )
    
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return hotel_to_display(new_hotel)


def get_hotel_db(db: Session, id: int):

    hotel = db.query(DbHotel).filter(DbHotel.id == id).first()
    if not hotel:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f'Could not find hotel with id: {id}')
    return hotel

def get_hotel(db: Session, id: int):
    hotel = get_hotel_db(db, id)
    hotel.rating = calculate_average_rating(hotel.ratings)
    return hotel_to_display(hotel)


def get_all_hotels(db: Session):
    hotels = db.query(DbHotel).all()
    if not hotels:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f'Could not find any hotels.')

    for hotel in hotels:
        hotel.rating = calculate_average_rating(hotel.ratings)
    return hotels


# update hotel
def update_hotel(db: Session, id: int, request: HotelBase, current_user):
    hotel = db.query(DbHotel).filter(DbHotel.id == id).first()
    if hotel is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f'Could not find hotel with id: {id}')
    hotel.name = request.name.lower()
    hotel.city = request.city.lower()
    hotel.address = request.address
    hotel.email = request.email
    hotel.phone_number = request.phone_number
    hotel.description = request.description
    hotel.available = request.available
    hotel_ratings = hotel.ratings
    hotel.rating = calculate_average_rating(hotel_ratings) 

    if not request.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hotel name cannot be empty."
        )
    
    if not request.city.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City cannot be empty."
        )
    
    if not request.address.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address cannot be empty."
        )
    
    if current_user.id != hotel.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this hotel."
        )
    
    db.commit()
    db.refresh(hotel)
    return hotel_to_display(hotel)

# delete hotel
def delete_hotel(db:Session, id:int,current_user):
    """Delete hotel and associated ratings"""
    hotel= db.query(DbHotel).filter(DbHotel.id == id).first()
    if hotel is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f'Could not find hotel with id: {id}')
    
    if current_user.id != hotel.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this hotel."
        )
    
    try:
        hotel_name = hotel.name
    except:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f'Could not find owner of hotel with id: {id}')
    db.query(DbRating).filter(DbRating.hotel_id == id).delete()
    db.delete(hotel)
    db.commit()
    return {"detail": f"Hotel: {hotel_name} and associated ratings are deleted!"}