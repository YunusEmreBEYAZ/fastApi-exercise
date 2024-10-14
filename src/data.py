from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import DbUser, DbHotel, DbRoom, DbBooking
from db.hash import Hash
import datetime
from datetime import date


def create_admin_user():
    db: Session = SessionLocal()
    try:
        admin_user = db.query(DbUser).filter(DbUser.username == 'admin').first()
        if admin_user:
            print("Admin user already exists.")
            return
        new_admin = DbUser(
            username='admin',
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password=Hash.bcrypt("admin123"),
            date_of_birth=datetime.date(1990, 1, 1),
            gender='other',
            roles=['guest'],
            phone_number='1234567890',
            is_active=True,
            profile_picture=None,
            is_admin=True
        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print("Admin user created successfully.")
    except Exception as e:
        print(f"An error occurred while creating admin user: {e}")
    finally:
        db.close()


def create_hotel():
    db: Session = SessionLocal()
    try:
        # Check if hotel already exists
        hotel = db.query(DbHotel).filter(DbHotel.name == 'HotelOne').first()
        if hotel:
            print("Hotel already exists.")
            return

        # Create new hotel
        new_hotel = DbHotel(
            name='HotelOne',
            city='Amsterdam',
            address="'s-Gravenhekje 1A",
            description='Test hotel',
            user_id=3,  # Assuming user_id is available and valid
            available=True,
            email='hotel_one@gmail.com',
            phone_number='123456789'
        )

        new_hotel_two = DbHotel(
            name='HotelTwo',
            city='Amsterdam',
            address="'s-Gravenhekje 1A",
            description='Test hotel',
            user_id=3,  # Assuming user_id is available and valid
            available=False,
            email='hotel_one@gmail.com',
            phone_number='123456789'
        )

        db.add(new_hotel)
        db.add(new_hotel_two)
        db.commit()
        db.refresh(new_hotel)

        # Create associated rooms for the new hotel
        rooms = [
            DbRoom(rooms_amount=5, guests_count=1, status=True, hotel_id=new_hotel.id),
            DbRoom(rooms_amount=10, guests_count=2, status=True, hotel_id=new_hotel.id),
            DbRoom(rooms_amount=5, guests_count=3, status=True, hotel_id=new_hotel.id),
            DbRoom(rooms_amount=5, guests_count=4, status=False, hotel_id=new_hotel.id)
        ]

        for room in rooms:
            db.add(room)

        db.commit()

        print("Hotel and associated rooms created successfully.")

    except Exception as e:
        print(f"An error occurred while creating hotel: {e}")

    finally:
        db.close()


def create_dummy_bookings():
    db: Session = SessionLocal()
    try:

        booking = db.query(DbBooking).filter(DbBooking.additional_info == 'Early check-in requested').first()
        if booking:
            print("Booking already exists.")
            return

        # Dummy booking data
        bookings = [
            DbBooking(
                checkin=date(2024, 10, 1),
                checkout=date(2024, 10, 5),
                rooms_amount=1,
                guests_count=2,
                additional_info="Early check-in requested",
                client_id=1,
                last_modifier_user_id=1,
                hotel_id=1,
                room_id=2
            ),
            DbBooking(
                checkin=date(2024, 10, 1),
                checkout=date(2024, 10, 5),
                rooms_amount=2,
                guests_count=4,
                additional_info="Regular check-in requested",
                client_id=2,
                last_modifier_user_id=2,
                hotel_id=1,
                room_id=2
            )
        ]

        # Add bookings to the session and commit
        for booking in bookings:
            db.add(booking)

        db.commit()
        print("Dummy bookings created successfully.")

    except Exception as e:
        print(f"An error occurred while creating bookings: {e}")

    finally:
        db.close()


def create_dummy_users():
    db: Session = SessionLocal()
    try:
        dummy_users = [
            {
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": Hash.bcrypt("john123"),
                "date_of_birth": datetime.date(1992, 5, 15),
                "gender": "male",
                "roles": ["guest"],
                "phone_number": "5551234567",
                "is_active": True,
                "profile_picture": None,
                "is_admin": False
            },
            {
                "username": "jane_smith",
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "password": Hash.bcrypt("jane123"),
                "date_of_birth": datetime.date(1995, 8, 22),
                "gender": "female",
                "roles": ["guest"],
                "phone_number": "5559876543",
                "is_active": True,
                "profile_picture": None,
                "is_admin": False
            },
            {
                "username": "alex_jones",
                "first_name": "Alex",
                "last_name": "Jones",
                "email": "alex.jones@example.com",
                "password": Hash.bcrypt("alex123"),
                "date_of_birth": datetime.date(1990, 12, 1),
                "gender": "other",
                "roles": ["guest"],
                "phone_number": "5557654321",
                "is_active": True,
                "profile_picture": None,
                "is_admin": False
            }
        ]

        for user_data in dummy_users:

            existing_user = db.query(DbUser).filter(DbUser.username == user_data["username"]).first()
            if existing_user:
                print(f"User {user_data['username']} already exists.")
                continue

            new_user = DbUser(
                username=user_data["username"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
                password=user_data["password"],
                date_of_birth=user_data["date_of_birth"],
                gender=user_data["gender"],
                roles=user_data["roles"],
                phone_number=user_data["phone_number"],
                is_active=user_data["is_active"],
                profile_picture=user_data["profile_picture"],
                is_admin=user_data["is_admin"]
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            print(f"User {user_data['username']} created successfully.")

    except Exception as e:
        print(f"An error occurred while creating dummy users: {e}")
    finally:
        db.close()
