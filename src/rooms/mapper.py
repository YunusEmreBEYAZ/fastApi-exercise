from rooms.dto import RoomRequest, RoomDto
from db.models import DbRoom, DbHotel


def db_room_to_dto(entity: DbRoom):
    result = RoomDto(
        id=entity.id,
        status=entity.status,
        rooms_amount=entity.rooms_amount,
        guests_count=entity.guests_count,
        hotel=entity.hotel
    )
    return result


def room_request_to_db(request: RoomRequest, hotel: DbHotel, db: DbRoom = None):
    if db is None:
        db = DbRoom()
    db.hotel_id = hotel.id
    db.hotel = hotel
    db.guests_count = request.guests_count
    db.rooms_amount = request.rooms_amount
    db.status = request.status
    return db

