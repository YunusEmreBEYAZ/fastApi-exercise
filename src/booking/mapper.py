from db.models import DbBooking
from booking.dto import BookingDto, BookingPostRequest
from db.models import DbUser, DbHotel
from db.booking_status_enum import BookingStatusEnum


def db_booking_to_dto(entity: DbBooking):

    result = BookingDto(
        id=entity.id,
        status=entity.status,
        date_start=entity.date_start,
        date_end=entity.date_end,
        room_amount=entity.room_amount,
        guests_count=entity.guests_count,
        additional_info=entity.additional_info,
        client_username=entity.client.username,
        hotel=entity.hotel
    )
    return result


def booking_request_to_db(request: BookingPostRequest, user: DbUser, hotel: DbHotel, db: DbBooking = None):
    if db is None:
        db = DbBooking()
    db.date_start = request.date_start
    db.date_end = request.date_end
    db.room_amount = request.room_amount
    db.guests_count = request.guests_count
    db.additional_info = request.additional_info
    db.client = user
    db.client_id = user.id
    db.hotel = hotel
    db.hotel_id = request.hotel_id
    db.status = BookingStatusEnum.draft
    return db
