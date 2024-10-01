from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser, DbHotel
from db.hash import Hash
from fastapi import HTTPException, status
from datetime import date


def calculate_age(date_of_birth: date) -> int:
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age

def create_user(db : Session, request: UserBase):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username: '{request.username}' is already taken."
        )
    
    user_age = calculate_age(request.date_of_birth)

    if user_age < 18:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be at least 18 years old to create an account!"
        )
    
    email = db.query(DbUser).filter(DbUser.email == request.email).first()
    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email: '{request.email}' is already taken."
        )

    new_user = DbUser (
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password),
        first_name = request.first_name,
        last_name = request.last_name,
        date_of_birth = request.date_of_birth,
        gender = request.gender,
        phone_number = request.phone_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db : Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Username: {username} is not found !")
    return user

def get_user_by_id(db : Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User ID: {id} is not found !")
    return user

def update_user(db : Session, username: str, request: UserBase):
    user = db.query(DbUser).filter(DbUser.username == username)
    if not user.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Username: {username} is not found !")
    
    user_age = calculate_age(request.date_of_birth)

    if user_age < 18:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be at least 18 years old to create an account!"
        )
    
    email = db.query(DbUser).filter(DbUser.email == request.email).first()
    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email: '{request.email}' is already taken."
        )

    user.update({
        DbUser.username : request.username,
        DbUser.email : request.email,
        DbUser.password : Hash.bcrypt(request.password),
        DbUser.first_name : request.first_name,
        DbUser.last_name : request.last_name,
        DbUser.date_of_birth : request.date_of_birth,
        DbUser.gender : request.gender,
        DbUser.phone_number : request.phone_number
    })
    db.commit()
    return f"User: {user.first().first_name} {user.first().last_name} Updated!"

def update_user_by_id(db : Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User ID: {id} is not found !")
    
    user_age = calculate_age(request.date_of_birth)

    if user_age < 18:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be at least 18 years old to create an account!"
        )
    
    email = db.query(DbUser).filter(DbUser.email == request.email).first()
    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email: '{request.email}' is already taken."
        )
     
    user.update({
        DbUser.username : request.username,
        DbUser.email : request.email,
        DbUser.password : Hash.bcrypt(request.password),
        DbUser.first_name : request.first_name,
        DbUser.last_name : request.last_name,
        DbUser.date_of_birth : request.date_of_birth,
        DbUser.gender : request.gender,
        DbUser.phone_number : request.phone_number
    })
    db.commit()
    return f"User: {user.first().first_name} {user.first().last_name} Updated!"

def delete_user(db : Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Username: {username} is not found !")

    db.delete(user)
    db.commit()
    return f"User: {user.first_name} {user.last_name} Deleted!"

def delete_user_by_id(db : Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User ID: {id} is not found !")
    
    db.query(DbHotel).filter(DbHotel.user_id == id).delete()

    db.delete(user)
    db.commit()
    return f"User: {user.first_name} {user.last_name} and associated hotels are Deleted!"
