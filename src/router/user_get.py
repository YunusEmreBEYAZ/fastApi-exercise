from fastapi import APIRouter, Depends
from schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user

router = APIRouter(
    prefix= '/user',
    tags= ['user']
)


@router.get('/username/{username}', response_model=UserDisplay, 
            summary="Get User by Username" 
        )
def get_user(username: str, db: Session = Depends(get_db)):
    """
        Fetches a user's details by their unique username. The username is provided as a path parameter.

        This endpoint will return the user's public information, such as:
        1. **First Name**
        2. **Last Name**
        3. **Email**

        If the user with the specified username does not exist, an HTTP 404 error will be returned.
    """
    return db_user.get_user(db, username)

@router.get('/id/{id}', response_model=UserDisplay,
                summary="Get User by ID", 
            )
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    """
        Fetches a user's details by their unique ID. The user ID is provided as a path parameter.

        This endpoint will return the user's public information such as:
        1. **First Name**
        2. **Last Name**
        3. **Email**

        If the user with the specified ID does not exist, an **HTTP 404** error will be returned.
    """
    return db_user.get_user_by_id(db, id)

@router.delete('/delete/username/{username}',                
               summary="Delete User by Username"
            )
def delete_user(username: str, db: Session = Depends(get_db)):
    """
        Deletes a user from the database based on their unique username. The username is provided as a path parameter. This action is permanent and will remove the user and all associated data from the system.

        Deletion Requirements:
        
        1. **Valid Username**: The user with the provided username must exist in the system.

        Error Handling:
        - Returns an **HTTP 404** error if the user with the given username does not exist.

        Upon successful deletion, the user and all associated data are permanently removed from the system, and a confirmation message is returned.
    """
    return db_user.delete_user(db, username)

@router.delete('/delete/id/{id}',
                summary="Delete User by ID" 
            )
def delete_user(id: int, db: Session = Depends(get_db)):
    """
        Deletes a user from the system based on their unique ID. The ID is provided as a path parameter. This action is permanent and will remove the user and all associated data from the system.

        Deletion Requirements:
        
        1. **Valid User ID**: The user with the provided ID must exist in the system.
        
        Error Handling:
        - Returns an **HTTP 404** error if the user with the given ID does not exist.
        
        Upon successful deletion, the user and their associated data are permanently removed from the system, and a confirmation message is returned.
    """
    return db_user.delete_user_by_id(db, id)