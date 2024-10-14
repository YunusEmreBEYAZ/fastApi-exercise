import functools

from sqlalchemy.orm.session import Session
from sqlalchemy import select, and_
from typing import List, Optional
from db.models import DbRoom, DbHotel, DbUser, DbBooking
from booking.dto import BookingPostRequest


class RoomsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, room_id: int) -> Optional[DbRoom]:
        return self.db.get(DbRoom, room_id)

    def get_by_hotel_id_and_guests_count(self, hotel_id: int, guests_count: int) -> Optional[DbRoom]:
        return next(iter(self.get_rooms_by_hotel_id(hotel_id, guests_count)), None)

    def get_available_rooms_count(self, request: BookingPostRequest) -> Optional[int]:
        occupied_count = self.get_occupied_rooms_count(request)
        if occupied_count is None:
            return None
        room = self.get(request.room_id)
        return room.rooms_amount - occupied_count

    def get_occupied_rooms_count(self, request: BookingPostRequest) -> Optional[int]:
        room = self.get(request.room_id)
        if room is None:
            return None
        bookings = (self.db.query(DbBooking)
                    .filter(DbBooking.room_id == room.id)
                    .filter(
            and_(DbBooking.checkin < request.checkout,
                 DbBooking.checkout > request.checkin
                 )
        ).all())
        bookings_rooms_amounts = list(map(lambda booking: booking.rooms_amount, bookings))
        if len(bookings_rooms_amounts) == 0:
            bookings_rooms_amounts = [0]
        return max(bookings_rooms_amounts)

    def get_rooms_by_hotel_id(self, hotel_id: int, guests_count: Optional[int] = None):
        return (self.db.query(DbRoom)
                .filter(DbRoom.hotel_id == hotel_id)
                .filter(True if guests_count is None else DbRoom.guests_count == guests_count)
                .all())

    def add(self, room: DbRoom) -> DbRoom:
        self.db.add(room)
        return room

    def remove(self, room: DbRoom) -> None:
        self.db.delete(room)
