from datetime import date
from typing import Optional
from booking.repository import BookingRepository
from booking.dto import BookingDto, BookingPostRequest
from db.database import get_db
from booking.mapper import db_booking_to_dto, booking_request_to_db
from booking.exceptions import BookingNotFoundException, BookingException
from exceptions import InconsistentDatesException, DatesException
from db.db_user import get_user
from db.db_hotel import get_hotel_db
from fastapi import HTTPException, status
from db.models import DbUser, DbHotel, DbRoom, DbBooking
from schemas import UserBase
from rooms.repository import RoomsRepository
from sqlalchemy.orm import make_transient


class BookingService:
    def __init__(self, current_user: UserBase):
        self.db = next(get_db())
        self.repository = BookingRepository(self.db)
        self.rooms_repository = RoomsRepository(self.db)
        self.current_user = current_user

    def get_all(self):
        db_bookings = self.repository.get_all()
        result = []
        for db_booking in db_bookings:
            result.append(db_booking_to_dto(db_booking))
        return result

    def get_bookings_by_username(self, username: str):
        db_bookings = self.repository.get_bookings_by_username(username)
        result = []
        for db_booking in db_bookings:
            result.append(db_booking_to_dto(db_booking))
        return result

    def get_bookings_by_hotels_username(self, username: str):
        db_bookings = self.repository.get_bookings_by_hotels_username(username)
        result = []
        for db_booking in db_bookings:
            result.append(db_booking_to_dto(db_booking))
        return result

    def get_by_id(self, booking_id):
        db_booking = self.repository.get(booking_id)
        if db_booking is None:
            raise BookingNotFoundException(f"Booking with id {booking_id} not found.")
        return db_booking_to_dto(db_booking)

    def add_current_user(self, booking: BookingPostRequest):
        return self.add(booking, self.current_user)

    def create_for_user(self, booking: BookingPostRequest, username: str):
        db_current_user = get_user(self.db, self.current_user.username)
        if not db_current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User {self.current_user.username} is forbidden to book for another user"
            )
        user = get_user(self.db, username)
        return self.add(booking, user)

    def add(self, booking: BookingPostRequest, user: UserBase):
        check_dates(booking)
        user = get_user(self.db, user.username)
        check_user_is_active(user)
        hotel = self.get_hotel_by_id(booking.hotel_id)
        check_hotel_is_active(hotel)
        room = self.get_room(booking.room_id, hotel)
        self.check_rooms_availability(booking)
        db_booking = booking_request_to_db(booking, user, hotel, room)
        new_booking = self.repository.add(db_booking)
        self.db.commit()
        self.db.refresh(new_booking)
        response_dto = db_booking_to_dto(new_booking)
        return response_dto

    def update(self, id: int, booking: BookingPostRequest):
        current_booking = self.get_by_id(id)
        check_dates(booking)
        current_db_booking = self.repository.get(id)
        self.repository.remove(current_db_booking)
        self.db.flush()
        self.check_rooms_availability(booking)
        current_db_booking = DbBooking()
        current_db_booking.id = id
        self.check_booking_authorization(id, self.current_user.username, 'update')
        hotel = self.get_hotel_by_id(booking.hotel_id)
        if hotel.id != current_booking.hotel.id:
            raise BookingException(f"Cannot change hotel from '{current_booking.hotel.name} "
                                   f"id={current_booking.hotel.id}' to '{hotel.name} id={hotel.id}'")
        room = self.get_room(booking.room_id, hotel)

        user = get_user(self.db, self.current_user.username)
        booking_request_to_db(booking, user, hotel, room, current_db_booking)
        self.repository.add(current_db_booking)
        self.db.commit()
        self.db.refresh(current_db_booking)
        return db_booking_to_dto(current_db_booking)

    def remove(self, booking_id: int):
        booking = self.get_by_id(booking_id)
        self.check_booking_authorization(booking_id, booking.client_username, 'remove')
        db_booking = self.repository.get(booking_id)
        self.repository.remove(db_booking)
        self.db.commit()

    def get_hotel_by_id(self, id: int):
        hotel = get_hotel_db(self.db, id)
        if hotel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hotel with id '{id}' not found."
            )
        return hotel

    def check_rooms_availability(self, request: BookingPostRequest):
        needed_rooms_amount = request.rooms_amount
        available_count = self.rooms_repository.get_available_rooms_count(request)
        if (available_count - needed_rooms_amount) < 0:
            hotel = get_hotel_db(self.db, request.hotel_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Hotel '{hotel.name}' doesn't have enough rooms available "
                       f"(needed count is {needed_rooms_amount} "
                       f"and available count is {available_count})"
            )

    def check_booking_authorization(self, booking_id: int, booking_usernames: list[str], action: str):
        if self.current_user.username not in booking_usernames:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User {self.current_user.username} is forbidden to {action} booking with id={booking_id}"
            )

    def get_room(self, room_id: int, hotel: DbHotel):
        room = self.rooms_repository.get(room_id)
        if room is None:
            raise BookingException(f"Room with id={room_id} not found")
        if room.hotel_id != hotel.id:
            raise BookingException(f"Room with id={room_id} does not belong to hotel {hotel.name} id={hotel.id}")
        if not room.status:
            raise BookingException(f"Room for {room.guests_count} guests in Hotel '{hotel.name}' is not available")
        return room


def check_dates(booking: BookingPostRequest):

    if booking.checkin >= booking.checkout:
        raise InconsistentDatesException(f"Dates are inconsistent (start '{booking.checkin}' >= end "
                                         f"'{booking.checkout}')")

    if booking.checkin < date.today():
        raise DatesException(f"Impossible to make booking in the past ({booking.checkin} < {date.today()})")


def check_user_is_active(user: DbUser):
    if not user.is_active:
        raise BookingException(f"User '{user.username}' is not active")


def check_hotel_is_active(hotel: DbHotel):
    if not hotel.available:
        raise BookingException(f"Hotel '{hotel.name}' is not available")
    if not hotel.owner.is_active:
        raise BookingException(f"Owner '{hotel.owner.username}' of '{hotel.name}' is not active")
