from datetime import date
from db.database import get_db
from db.db_user import get_user
from fastapi import HTTPException, status
from db.models import DbUser, DbHotel
from schemas import UserBase
from rooms.repository import RoomsRepository
from rooms.dto import RoomRequest
from rooms.mapper import room_request_to_db, db_room_to_dto
from db.db_hotel import get_hotel_db
from typing import Optional
from booking.dto import BookingPostRequest


class RoomsService:
    def __init__(self, current_user: UserBase):
        self.db = next(get_db())
        self.repository = RoomsRepository(self.db)
        self.current_user = current_user

    def get_rooms_by_hotel_id(self, hotel_id: int):
        db_rooms = self.repository.get_rooms_by_hotel_id(hotel_id)
        result = []
        for db_room in db_rooms:
            result.append(db_room_to_dto(db_room))
        return result

    def get_room_by_id(self, room_id: int):
        db_room = self.repository.get(room_id)
        return db_room_to_dto(db_room)

    def get_available_rooms_by_hotel_id_and_period(self, hotel_id: int, checkin: date, checkout: date):
        request = BookingPostRequest(hotel_id=hotel_id, checkin=checkin, checkout=checkout,
                                     room_id=1, rooms_amount=1, guests_count=1)
        list = self.get_rooms_by_hotel_id(hotel_id)
        for room in list:
            request.room_id = room.id
            room.rooms_amount = self.repository.get_available_rooms_count(request)
        return list

    def create_new_room(self, hotel_id: int, room: RoomRequest):
        db_hotel = get_hotel_db(self.db, hotel_id)
        self.check_hotel_user(db_hotel)
        db_room = room_request_to_db(room, db_hotel)
        self.check_room_of_type_exists(None, room, hotel_id)
        self.repository.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room_to_dto(db_room)

    def update(self, room_id: int, room: RoomRequest):
        db_room = self.repository.get(room_id)
        self.check_hotel_user(db_room.hotel)
        self.check_room_of_type_exists(room_id, room, db_room.hotel.id)
        room_request_to_db(room, db_room.hotel, db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room_to_dto(db_room)

    def remove(self, room_id: int):
        db_room = self.repository.get(room_id)
        if db_room is None:
            HTTPException(status=HTTP_404_NOT_FOUND,
                          detail=f"Rooms with id={room_id} not found")
        self.check_hotel_user(db_room.hotel)
        self.repository.remove(db_room)
        self.db.commit()

    def check_room_of_type_exists(self, room_id: Optional[int], room: RoomRequest, hotel_id: int):
        db_room = self.repository.get_by_hotel_id_and_guests_count(hotel_id, room.guests_count)
        if (not (db_room is None)) and (room_id != db_room.id or room_id is None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Rooms with guests count {db_room.guests_count} already exists"
                                       f" in the hotel with id='{hotel_id}'")

    def check_hotel_user(self, hotel: DbHotel):
        if hotel.owner.username != self.current_user.username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User {self.current_user.username} cannot edit rooms of hotel '{hotel.name}'")

