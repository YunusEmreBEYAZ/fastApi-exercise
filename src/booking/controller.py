from fastapi import APIRouter, Depends, status
from booking.service import BookingService
from booking.dto import BookingDto, BookingPostRequest
from auth.oauth2 import get_current_user
from schemas import UserBase

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


@router.get('/list',
            summary='Retrieve list of all bookings',
            description='Retrieve list of all bookings from the application''s database',
            response_description="List of all bookings")
def get_all_bookings(current_user: UserBase = Depends(get_current_user)):
    service = BookingService(current_user)
    return service.get_all()


@router.get('/list_my_bookings',
            summary='Retrieve list of all bookings made by current user',
            description='Retrieve list of all bookings made by current user from the application''s database',
            response_description="List of all my bookings")
def get_all_my_bookings(current_user: UserBase = Depends(get_current_user)):
    service = BookingService(current_user)
    return service.get_bookings_by_username(current_user.username)


@router.get('/list_my_hotels_bookings',
            summary='Retrieve list of all bookings made for current user''s hotels',
            description='Retrieve list of all bookings made for current user''s hotels '
                        'from the application''s database',
            response_description="List of all bookings for my hotels")
def get_my_hotels_bookings(current_user: UserBase = Depends(get_current_user)):
    service = BookingService(current_user)
    return service.get_bookings_by_hotels_username(current_user.username)


@router.get('/{booking_id}',
            summary='Retrieve booking by id',
            description='Retrieve booking by id from the application''s database',
            response_description="Booking")
def get_booking_by_id(booking_id: int, current_user: UserBase = Depends(get_current_user)):
    service = BookingService(current_user)
    return service.get_by_id(booking_id)


@router.post('/create_for_user',
             response_model=BookingDto,
             summary='Create new booking with given parameters for given user',
             description='Create new booking with given parameters for given user',
             response_description="New created booking with id for given user",
             status_code=status.HTTP_201_CREATED)
def create_for_user(username: str, request: BookingPostRequest, current_user: UserBase = Depends(get_current_user)):
    service = BookingService(current_user)
    return service.create_for_user(request, username)


@router.post('/',
             response_model=BookingDto,
             summary='Create new booking with given parameters',
             description='Create new booking with given parameters',
             response_description="New created booking with id",
             status_code=status.HTTP_201_CREATED)
def add(request: BookingPostRequest, current_user: UserBase = Depends(get_current_user)):
    service = BookingService(current_user)
    return service.add_current_user(request)


@router.put('/{booking_id}',
            response_model=BookingDto,
            summary='Update existed booking with given parameters',
            description='Update existed booking in the application''s database with given parameters',
            response_description="Updated booking",
            status_code=status.HTTP_200_OK)
def update(booking_id: int, request: BookingPostRequest, current_user: UserBase = Depends(get_current_user)):
    service = BookingService(current_user)
    return service.update(booking_id, request)


@router.delete('/{booking_id}',
               summary='Delete booking by id',
               description='Delete booking by id from the application''s database',
               response_description="Returns HTTP status = 204",
               status_code=status.HTTP_204_NO_CONTENT)
def remove(booking_id: int, current_user: UserBase = Depends(get_current_user)):
    service = BookingService(current_user)
    service.remove(booking_id)
