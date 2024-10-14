from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser, DbHotel
from db.hash import Hash
from fastapi import HTTPException, status
from datetime import date
import shutil
from datetime import datetime
from exception.user import get_admin_exception, get_credentials_exception

def calculate_age(date_of_birth: date) -> int:
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age

def check_current_user(current_user):
    if current_user is None:
        raise get_credentials_exception()


def get_all_user(db : Session, current_user: DbUser, usernameFilter, is_admin_filter):

    users = db.query(DbUser)
    
    if usernameFilter is not None:
        users = users.filter(DbUser.username == usernameFilter)
        if not users.first():
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Username: {usernameFilter} is not found!")
        elif users.first().username != current_user.username and not current_user.is_admin:
            raise get_admin_exception()
    elif usernameFilter is None and  not current_user.is_admin:
        raise get_admin_exception()

    if is_admin_filter is not None and current_user.is_admin:
        users = users.filter(DbUser.is_admin == is_admin_filter)
        if not users.first():
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User admin: {is_admin_filter} is not found, use true or false!")
    elif is_admin_filter is not None and not current_user.is_admin:
            raise get_admin_exception()

    return users.all()

def get_user_by_id(db : Session, id: int, current_user: DbUser):

    if id is not None:
        user = db.query(DbUser).filter(DbUser.id == id).first()
        if not user:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User ID: {id} is not found !")
        elif user.id != current_user.id and not current_user.is_admin:
            raise get_admin_exception()
    elif id is None and  not current_user.is_admin:
        raise get_admin_exception()
     
    return user

def upload_file(upload_file, db : Session, current_user):

    if upload_file.filename:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        path = f'files/{timestamp}_{upload_file.filename}'
        with open(path, 'w+b') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        current_user.profile_picture = path
    else: 
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    valid_image_types = [
        "image/jpeg",  # JPEG
        "image/jpg",   # JPG
        "image/png",   # PNG
        "image/gif",   # GIF
        "image/bmp",   # BMP
        "image/tiff",  # TIFF
        "image/webp"   # WEBP
    ]
    
    if upload_file.content_type not in valid_image_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {upload_file.content_type}. Only JPEG, PNG, GIF, BMP, TIFF, and WEBP images are allowed."
        )
    db.commit()
    db.refresh(current_user)
    return {
            "info": "Profile picture uploaded successfully", 
            "file_path": path
        }

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
        phone_number = request.phone_number,
        profile_picture = None  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        'message' : f'User with username: {new_user.username} is created succesfully!',
        'first/last name' : f'{new_user.first_name} {new_user.last_name}',
        'email' : f'{new_user.email}' 
    }

def get_user(db : Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Username: {username} is not found !")
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

def update_user_by_id(db : Session, id: int, request: UserBase, current_user: DbUser):
    if id is not None:
        user = db.query(DbUser).filter(DbUser.id == id)
        if not user.first():
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User ID: {id} is not found !")
        elif id != current_user.id and not current_user.is_admin:
            raise get_admin_exception()
    elif id is None and  not current_user.is_admin:
        raise get_admin_exception()
    
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
     
    update_data = {
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password),
        DbUser.first_name: request.first_name,
        DbUser.last_name: request.last_name,
        DbUser.date_of_birth: request.date_of_birth,
        DbUser.gender: request.gender,
        DbUser.phone_number: request.phone_number,
        DbUser.is_admin: request.is_admin
    }
    if request.is_admin != current_user.is_admin and not current_user.is_admin:
        raise get_admin_exception()

    user.update(update_data)        
    db.commit()
    return f"User: {user.first().first_name} {user.first().last_name} Updated!"

def delete_user(db : Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Username: {username} is not found !")

    db.delete(user)
    db.commit()
    return f"User: {user.first_name} {user.last_name} Deleted!"

def delete_user_by_id(db : Session, id: int, current_user: DbUser):
    if id is not None:
        user = db.query(DbUser).filter(DbUser.id == id).first()
        if not user:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User ID: {id} is not found !")
        elif user.id != current_user.id and not current_user.is_admin:
            raise get_admin_exception()
    elif id is None and  not current_user.is_admin:
        raise get_admin_exception() 
    db.query(DbHotel).filter(DbHotel.user_id == id).delete()

    db.delete(user)
    db.commit()
    return f"User: {user.first_name} {user.last_name} and associated hotels are Deleted!"

def is_admin(current_user: UserBase):
    if not current_user.is_admin:
        raise get_admin_exception()

def assign_admin(db : Session, id: int, current_user: UserBase):

    is_admin(current_user)

    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found."
        )
    
    user.is_admin = True
    db.commit()
    db.refresh(user)
    
    return {"detail": f"User {user.username} has been assigned admin privileges."}

