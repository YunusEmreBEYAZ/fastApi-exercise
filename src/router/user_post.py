from fastapi import APIRouter, Depends, UploadFile, File
from schemas import UserBase, UserDisplay, UserBaseAdmin
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix= '/users',
    tags= ['users']
)

@router.post('/',
                summary="Create a New User"
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


@router.post('/profile-picture',
                summary="Upload a new user profile picture")

def upload_file(upload_file : UploadFile = File(...),     
                db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)
            ):
    """
        Uploads a profile picture for the authenticated user.

        This function accepts an uploaded file and saves it to a specified location on the server.
        Before saving, it checks if the uploaded file is an image (`JPEG`, `PNG`, `GIF`, `BMP`, `TIFF`). 
        If the file type is not supported, an **HTTP 400** error is raised.

        **Returns**:
        A success message and the path to the uploaded file.

        **Raises**:
        - **HTTP 400**: If no file is uploaded or if the file is not an image.
    """
    db_user.check_current_user(current_user)
    return db_user.upload_file(upload_file, db, current_user)

@router.put('/{id}',
                summary="Update User Information by ID", )
def update_user_by_id(id : int,request: UserBaseAdmin, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    """
        Updates the details of an existing user identified by their unique ID. This endpoint allows an authenticated user to update their own details or an admin to update any user's details. Admins also have the exclusive ability to assign or unassign admin roles.

        Update Requirements:

        1. **Authentication Required**: The user must be authenticated to access this endpoint.
        2. **User Self-Service**: Authenticated users can only update their own details unless they have admin privileges.
        3. **Admin Privileges**: Admins can update details for any user and manage admin roles. Unauthorized role modifications result in an HTTP 403 Forbidden error.
        4. **Valid User ID**: The user with the provided ID must exist in the system. If not, an HTTP 404 error is returned.
        5. **Unique Email**: If the email is updated, it must be unique and not registered to any other user. An HTTP 400 error is raised if the email is already in use.
        6. **Age Requirement**: If the date of birth is updated, the user must be at least 18 years old. An HTTP 400 error is returned for underage users.
        7. **Secure Password**: If the password is updated, it is securely hashed using bcrypt.

        Error Handling:
        - **HTTP 404 Not Found**: Returned if no user exists with the given ID.
        - **HTTP 403 Forbidden**: Returned if an unauthorized user attempts to perform admin-specific actions or if a non-admin user attempts to update another user's details.
        - **HTTP 400 Bad Request**: Returned under conditions where email conflicts or age requirements are not met.

        Upon successful validation, the user's details are updated in the database.
    """
    db_user.check_current_user(current_user)
    return db_user.update_user_by_id(db, id, request, current_user)
