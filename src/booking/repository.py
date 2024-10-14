from sqlalchemy.orm.session import Session
from sqlalchemy import select
from typing import List, Optional
from db.models import DbBooking, DbHotel, DbUser


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, booking_id: int) -> Optional[DbBooking]:
        return self.db.get(DbBooking, booking_id)

    def get_all(self):
        return self.db.query(DbBooking).all()

    def get_bookings_by_hotels_username(self, user_name: str):
        return self.db.query(DbBooking).join(DbHotel).join(DbUser).filter(DbUser.username == user_name).all()

    def get_bookings_by_username(self, user_name: str):
        return (self.db.query(DbBooking).join(DbUser, onclause=DbBooking.client_id == DbUser.id)
                .filter(DbUser.username == user_name).all())

    def add(self, booking: DbBooking) -> DbBooking:
        self.db.add(booking)
        return booking

    def remove(self, booking: DbBooking) -> None:
        self.db.delete(booking)
