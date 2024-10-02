from sqlalchemy.orm import Session
from db.models import DbHotel
from schemas import HotelBase
from fastapi import HTTPException, status

def create_hotel(db: Session, request: HotelBase):
    new_hotel = DbHotel(
        name= request.name.lower(),
        city= request.city.lower(),
        address= request.address,
        email= request.email,
        phone_number= request.phone_number,
        description= request.description,
        user_id= request.user_id
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
    
    if not request.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID cannot be empty."
        )
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel

def get_all_hotels(db:Session):
    hotels = db.query(DbHotel).all()
    return hotels

def get_hotel(db: Session, id: int):
    hotel = db.query(DbHotel).filter(DbHotel.id == id).first()
    if not hotel:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f'Could not find hotel with id: {id}')

    return hotel

def get_hotel_by_city(db: Session, city_name: str):
    hotels = db.query(DbHotel).filter(DbHotel.city == city_name.lower()).all()
    if not hotels:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f'Could not find hotels in city: {city_name}')
    return hotels

# update hotel
def update_hotel(db: Session, id: int, request: HotelBase):
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
    
    if not request.user_id or request.user_id != hotel.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can not change the owner of the hotel!"
        )
    db.commit()
    db.refresh(hotel)
    return hotel

# delete hotel
def delete_hotel(db:Session, id:int):
    hotel= db.query(DbHotel).filter(DbHotel.id == id).first()
    if hotel is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f'Could not find hotel with id: {id}')
    
    try:
        hotel_name = hotel.name
    except:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f'Could not find owner of hotel with id: {id}')
    db.delete(hotel)
    db.commit()
    return {"detail": f"Hotel: {hotel_name} is deleted successfully."}