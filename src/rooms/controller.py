import datetime
from fastapi import APIRouter, Depends, status
from auth.oauth2 import get_current_user
from rooms.dto import RoomDto, RoomRequest
from schemas import UserBase
from rooms.service import RoomsService


router = APIRouter(
    prefix='/rooms',
    tags=['rooms']
)


@router.get('/',
            summary='Retrieves list of all rooms in the given hotel',
            description='Retrieves list of all rooms from the application''s database',
            response_description="List of all rooms")
def get_rooms_by_hotel_id(hotel_id: int, current_user: UserBase = Depends(get_current_user)):
    service = RoomsService(current_user)
    return service.get_rooms_by_hotel_id(hotel_id)


@router.get('/get_available_rooms',
            summary='Retrieves list of all available rooms in the given hotel for given period',
            description='Retrieves list of all available rooms in the given hotel for given period'
                        ' from the application''s database',
            response_description="List of all available rooms")
def get_available_rooms_by_hotel_id_and_period(hotel_id: int, checkin: datetime.date, checkout: datetime.date,
                                               current_user: UserBase = Depends(get_current_user)):
    service = RoomsService(current_user)
    return service.get_available_rooms_by_hotel_id_and_period(hotel_id, checkin, checkout)


@router.get('/{room_id}',
            summary='Retrieves room by the given id in the given hotel',
            description='Retrieves room by the given id in the given hotel from the application''s database',
            response_description="Single room")
def get_room_by_id(room_id: int, current_user: UserBase = Depends(get_current_user)):
    service = RoomsService(current_user)
    return service.get_room_by_id(room_id)


@router.post('/rooms',
             summary='Creates new room for the given hotel',
             description='Creates new room for the given hotel in the application''s database',
             response_description="New created room")
def create_new_room(hotel_id: int, request: RoomRequest,  current_user: UserBase = Depends(get_current_user)):
    service = RoomsService(current_user)
    return service.create_new_room(hotel_id, request)


@router.put('/{room_id}',
            summary='Updates room with the given id for the given hotel',
            description='Updates room with the given id for the given hotel in the application''s database',
            response_description="Updated room")
def update_room(room_id: int, request: RoomRequest, current_user: UserBase = Depends(get_current_user)):
    service = RoomsService(current_user)
    return service.update(room_id, request)


@router.delete('/{room_id}',
               summary='Deletes room with the given id for the given hotel',
               description='Deletes room with the given id for the given hotel in the application''s database',
               response_description="Returns HTTP status = 204",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, current_user: UserBase = Depends(get_current_user)):
    service = RoomsService(current_user)
    service.remove(room_id)
