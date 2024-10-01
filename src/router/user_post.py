from fastapi import APIRouter, Depends
from schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user


router = APIRouter(
    prefix= '/user',
    tags= ['user']
)

@router.post('/', response_model= UserDisplay,
                          summary="Create a New User", 
            #  description="""
            #  Creates a new user in the system with the following requirements:
             
            #  1. **Unique Username**: The provided username must not already be taken. If the username exists, an error will be raised.
            #  2. **Unique Email**: The email address must be unique. If the email is already registered, an error will be raised.
            #  3. **Age Requirement**: The user must be at least 18 years old to create an account.
            #    An error is raised if the user does not meet this age requirement.
            #  4. **Secure Password**: The password will be hashed using bcrypt for security.

            #  Error Handling:
            #  - Returns an **HTTP 400** error if:
            #    - The username is already taken.
            #    - The email is already registered.
            #    - The user is under 18 years old.

            #  After passing all validations, the user information will be securely stored in the database.
            #  """
            )
def create_new_user(request: UserBase, db: Session = Depends(get_db)):
    """
        Creates a new user in the system with the following requirements:
        
        1. **Unique Username**: The provided username must not already be taken. If the username exists, an error will be raised.
        2. **Unique Email**: The email address must be unique. If the email is already registered, an error will be raised.
        3. **Age Requirement**: The user must be at least 18 years old to create an account.
        An error is raised if the user does not meet this age requirement.
        4. **Secure Password**: The password will be hashed using bcrypt for security.
        5. **Valid Gender**: The gender field must be one of the following: 'male', 'female', or 'other'.
        If an invalid gender value is provided, an error will be raised.

        Error Handling:
        - Returns an **HTTP 400** error if:
            - The username is already taken.
            - The email is already registered.
            - The user is under 18 years old.
        - Returns an **HTTP 422** error if:
            - An invalid value is provided for the gender field (e.g., 'XYZ' instead of 'male', 'female', or 'other').
        
        After passing all validations, the user information will be securely stored in the database.
    """
    return db_user.create_user(db, request)

@router.put('/username/{username}/update',
                        summary="Update User Information", 
            )
def update_user(username : str,request: UserBase, db: Session = Depends(get_db)):
    """
        Updates the details of an existing user. The username is provided as a path parameter and the user information in the request body.

        Update Requirements:
        
        1. **Valid Username**: The user with the provided username must exist in the system.
        2. **Unique Email**: If the email is being updated, it must not be registered to another user. An error is raised if the email is already in use.
        3. **Age Requirement**: If the date of birth is updated, the user must still meet the minimum age requirement of 18 years old.
        4. **Secure Password**: If the password is updated, it will be securely hashed using bcrypt.

        Error Handling:
        - Returns an **HTTP 404** error if the user with the given username does not exist.
        - Returns an **HTTP 400** error if:
            - The updated email is already registered with another user.
            - The user is under 18 years old after updating the date of birth.
        
        Upon successful validation, the user's details will be updated and stored in the database.
    """
    return db_user.update_user(db, username, request)

@router.put('/id/{id}/update',
                summary="Update User Information by ID", 
            )
def update_user_by_id(id : int,request: UserBase, db: Session = Depends(get_db)):
    """
        Updates the details of an existing user identified by their unique ID. The ID is provided as a path parameter and the user information in the request body.

        Update Requirements:
        
        1. **Valid User ID**: The user with the provided ID must exist in the system.
        2. **Unique Email**: If the email is being updated, it must not be registered to another user. An error is raised if the email is already in use.
        3. **Age Requirement**: If the date of birth is updated, the user must still meet the minimum age requirement of 18 years old.
        4. **Secure Password**: If the password is updated, it will be securely hashed using bcrypt.

        Error Handling:
        - Returns an **HTTP 404** error if the user with the given ID does not exist.
        - Returns an **HTTP 400** error if:
            - The updated email is already registered with another user.
            - The user is under 18 years old after updating the date of birth.
        
        Upon successful validation, the user's details will be updated and stored in the database.
    """
    return db_user.update_user_by_id(db, id, request)