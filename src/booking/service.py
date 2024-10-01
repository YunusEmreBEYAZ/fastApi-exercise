from datetime import date
from booking.repository import BookingRepository
from booking.dto import BookingDto, BookingPostRequest
from db.database import get_db
from db.booking_status_enum import BookingStatusEnum
from booking.mapper import db_booking_to_dto, booking_request_to_db
from booking.exceptions import BookingNotFoundException, BookingStatusException, BookingException
from exceptions import InconsistentDatesException, DatesException
from db.db_user import get_user
from db.db_hotel import get_hotel
from fastapi import HTTPException, status
from db.models import DbUser, DbHotel


class BookingService:
    def __init__(self):
        self.db = next(get_db())
        self.repository = BookingRepository(self.db)

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

    def add(self, booking: BookingPostRequest):
        check_dates(booking)
        user = get_user(self.db, booking.client_username)
        check_user_is_active(user)
        hotel = self.get_hotel_by_id(booking.hotel_id)
        check_hotel_is_active(hotel)
        db_booking = booking_request_to_db(booking, user, hotel)
        new_booking = self.repository.add(db_booking)
        self.db.commit()
        self.db.refresh(new_booking)
        response_dto = db_booking_to_dto(new_booking)
        return response_dto

    def update(self, id: int, booking: BookingPostRequest):
        current_booking = self.get_by_id(id)
        check_status_is_draft(current_booking)
        check_dates(booking)
        user = get_user(self.db, booking.client_username)
        if user.username != current_booking.client_username:
            raise BookingException(f"Cannot change username from "
                                   f"'{current_booking.client_username}' to '{user.username}'")
        hotel = self.get_hotel_by_id(booking.hotel_id)
        if hotel.id != current_booking.hotel.id:
            raise BookingException(f"Cannot change hotel from '{current_booking.hotel.name} "
                                   f"id={current_booking.hotel.id}' to '{hotel.name} id={hotel.id}'")
        current_db_booking = self.repository.get(id)
        booking_request_to_db(booking, user, hotel, current_db_booking)
        self.db.commit()
        self.db.refresh(current_db_booking)
        return db_booking_to_dto(current_db_booking)

    def remove(self, booking_id: int):
        booking = self.get_by_id(booking_id)
        check_status_is_draft(booking)
        db_booking = self.repository.get(booking_id)
        self.repository.remove(db_booking)
        self.db.commit()

    def confirm(self, booking_id: int):
        return self.set_next_status(booking_id, True)

    def cancel(self, booking_id: int):
        return self.set_next_status(booking_id, False)

    def undo_confirm(self, booking_id: int):
        booking = self.get_by_id(booking_id)
        check_status_is_confirmed(booking)
        return self.set_status(booking_id, BookingStatusEnum.draft)

    def undo_cancel(self, booking_id: int):
        booking = self.get_by_id(booking_id)
        check_status_is_canceled(booking)
        return self.set_status(booking_id, BookingStatusEnum.draft)

    def set_next_status(self, booking_id: int, is_approve: bool):
        booking = self.get_by_id(booking_id)
        check_status_is_draft(booking)
        status = BookingStatusEnum.confirmed if is_approve else BookingStatusEnum.canceled
        return self.set_status(booking_id, status)

    def get_hotel_by_id(self, id: int):
        hotel = get_hotel(self.db, id)
        if hotel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hotel with id '{id}' not found."
            )
        return hotel

    def set_status(self, booking_id: int, status: BookingStatusEnum):
        db_booking = self.repository.get(booking_id)
        db_booking.status = status
        self.db.commit()
        self.db.refresh(db_booking)
        return db_booking_to_dto(db_booking)


def check_status_is_draft(booking: BookingDto):
    check_status(booking, BookingStatusEnum.draft)


def check_status_is_confirmed(booking: BookingDto):
    check_status(booking, BookingStatusEnum.confirmed)


def check_status_is_canceled(booking: BookingDto):
    check_status(booking, BookingStatusEnum.canceled)


def check_status(booking: BookingDto, status: BookingStatusEnum):
    if booking.status != status:
        raise BookingStatusException(f"Booking should be {status.value}.")


def check_dates(booking: BookingPostRequest):
    if booking.date_start > booking.date_end:
        raise InconsistentDatesException(f"Dates are inconsistent (start '{booking.date_start}' > end "
                                         f"'{booking.date_end}')")

    if booking.date_start < date.today():
        raise DatesException(f"Impossible to make booking in the past ({booking.date_start} < {date.today()})")


def check_user_is_active(user: DbUser):
    if not user.is_active:
        raise BookingException(f"User '{user.username}' is not active")


def check_hotel_is_active(hotel: DbHotel):
    if not hotel.available:
        raise BookingException(f"Hotel '{hotel.name}' is not available")
    if not hotel.owner.is_active:
        raise BookingException(f"Owner '{hotel.owner.username}' of '{hotel.name}' is not active")
