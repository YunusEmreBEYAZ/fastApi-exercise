from db.models import DbBooking
from booking.dto import BookingDto, BookingPostRequest
from db.models import DbUser, DbHotel, DbRoom


def db_booking_to_dto(entity: DbBooking):

    result = BookingDto(
        id=entity.id,
        checkin=entity.checkin,
        checkout=entity.checkout,
        rooms_amount=entity.rooms_amount,
        guests_count=entity.guests_count,
        additional_info=entity.additional_info,
        client_username=entity.client.username,
        hotel=entity.hotel,
        room_id=entity.room.id,
        room_guests_count=entity.room.guests_count
    )
    return result


def booking_request_to_db(request: BookingPostRequest, user: DbUser,
                          hotel: DbHotel, room: DbRoom, db: DbBooking = None):
    if db is None:
        db = DbBooking()
    db.checkin = request.checkin
    db.checkout = request.checkout
    db.rooms_amount = request.rooms_amount
    db.guests_count = request.guests_count
    db.additional_info = request.additional_info
    db.client = user
    db.client_id = user.id
    db.last_modifier_user = user
    db.last_modifier_user_id = user.id
    db.hotel = hotel
    db.hotel_id = request.hotel_id
    db.room = room
    db.room_id = request.room_id
    return db
