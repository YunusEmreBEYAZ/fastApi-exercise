from db.database import Base
from sqlalchemy import Column, Enum, JSON, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.sql.sqltypes import Integer, String, Date, Boolean
from db.gender_enum import GenderEnum
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index= True)
    username = Column(String, unique= True, index= True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique= True)
    password = Column(String)
    date_of_birth = Column(Date)
    gender = Column(Enum(GenderEnum))
    roles = Column(JSON, default=["guest"])
    phone_number = Column(String(15)) # limit of 15 num
    is_active = Column(Boolean, default=True)
    profile_picture = Column(String, nullable=True)
    hotels = relationship("DbHotel", back_populates="owner")  # relationship with hotels table 
    bookings = relationship("DbBooking", foreign_keys='DbBooking.client_id', back_populates="client")
    is_admin = Column(Boolean, default=False)
    ratings = relationship("DbRating", back_populates="user")

    
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
    ratings = relationship("DbRating", back_populates="rated_hotel")
    user_id = Column(Integer, ForeignKey("users.id"))  # ForeignKey to users table
    owner = relationship("DbUser", back_populates="hotels")
    available = Column(Boolean, default=True)
    bookings = relationship("DbBooking", back_populates="hotel")  # Link to bookings



class DbBooking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    checkin = Column(Date)
    checkout = Column(Date)
    rooms_amount = Column(Integer)
    guests_count = Column(Integer)
    additional_info = Column(String)
    client_id = Column(Integer, ForeignKey("users.id"))
    client = relationship("DbUser", foreign_keys=[client_id], back_populates="bookings")
    last_modifier_user_id = Column(Integer, ForeignKey("users.id"))
    last_modifier_user = relationship("DbUser", foreign_keys=[last_modifier_user_id])
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    hotel = relationship("DbHotel", back_populates="bookings")
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("DbRoom")
    ratings = relationship("DbRating", back_populates="rated_booking")

class DbRating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    rating_score = Column(Integer)
    rating_date = Column(Date)
    title = Column(String)
    comment = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    rated_booking = relationship("DbBooking", back_populates="ratings")
    rated_hotel = relationship("DbHotel", back_populates="ratings")
    user = relationship("DbUser", back_populates="ratings")


class DbRoom(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, index=True)
    rooms_amount = Column(Integer)
    guests_count = Column(Integer)
    status = Column(Boolean)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    hotel = relationship("DbHotel")
    __table_args__ = (UniqueConstraint('hotel_id', 'guests_count', name='_room_uc'),)

