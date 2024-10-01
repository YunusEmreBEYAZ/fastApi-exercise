from db.database import Base
from sqlalchemy import Column, Enum, JSON, ForeignKey, CheckConstraint
from sqlalchemy.sql.sqltypes import Integer, String, Date, Boolean
from db.gender_enum import GenderEnum
from db.booking_status_enum import BookingStatusEnum
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index= True)
    username = Column(String, unique= True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique= True)
    password = Column(String)
    date_of_birth = Column(Date)
    gender = Column(Enum(GenderEnum))
    roles = Column(JSON, default=["guest"])
    phone_number = Column(String(15)) # limit of 15 num
    is_active = Column(Boolean, default=True)
    hotels = relationship("DbHotel", back_populates="owner")  # relationship with hotels table 
    rating = relationship("DbRating", back_populates="user")


class DbHotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    city = Column(String)
    address = Column(String)
    email = Column(String)
    phone_number = Column(String)
    description = Column(String)
    rating = Column(Integer , default=0)
    user_id = Column(Integer, ForeignKey("users.id"))  # ForeignKey to users table
    owner = relationship("DbUser", back_populates="hotels")
    available = Column(Boolean, default=True)


class DbBooking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    date_start = Column(Date)
    date_end = Column(Date)
    room_amount = Column(Integer)
    guests_count = Column(Integer)
    status = Column(Enum(BookingStatusEnum))
    additional_info = Column(String)
    client_id = Column(Integer, ForeignKey("users.id"))
    client = relationship("DbUser")
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    hotel = relationship("DbHotel")
    rating = relationship('DbRating', back_populates='booking')

class DbRating(Base):
    __tablename__ = 'ratings'
    rating_id = Column(Integer, primary_key=True, index= True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    booking = relationship('DbBooking', back_populates='rating')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('DbUser', back_populates='rating')
    rating_score = Column(Integer, CheckConstraint('rating_score >= 1 AND rating_score <= 5'), nullable=False)
    rating_date = Column(Date)

