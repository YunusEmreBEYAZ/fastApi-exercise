from fastapi import APIRouter, Depends
from schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user
from fastapi.responses import FileResponse
from fastapi import HTTPException, status
import os
from typing import List, Optional
from exception.user import get_credentials_exception, get_admin_exception


router = APIRouter(
    prefix= '/users',
    tags= ['users']
)


@router.get("", response_model=List[UserDisplay],
            summary="Get User By username or All Users (Admin Only) ")
def get_all_users(
    username: Optional[str] = None,
    is_admin: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    """
    Retrieves a user by username or all users from the database. Additionally, the admins only can retrieve a list of all admin and non-admin users.

    **Requirements**:

    - **Authenticated  User**: can access the user details by username.
    - **Authenticated Admin User**: Only users with admin privileges can access all users list.

    **Returns**:

    - A list of users with their details.

    **Raises**:

    - **HTTP 403 Forbidden**: If the requester is not an admin.
    - **HTTP 404 error**: If the user with the specified username does not exist.

    """
    db_user.check_current_user(current_user)
    return db_user.get_all_user(db, current_user, username, is_admin)

@router.get('/{id}',
                summary="Get User by ID",
                response_model= UserDisplay)

def get_user_by_id(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    """
        Fetches a user's details by their unique ID. The user ID is provided as a path parameter.

        This endpoint will return the user's public information such as:
        1. **First Name**
        2. **Last Name**
        3. **Email**

        If the user with the specified ID does not exist, an **HTTP 404** error will be returned.
    """   
    db_user.check_current_user(current_user)
    return db_user.get_user_by_id(db, id, current_user)


@router.get('/{id}/profile-picture/', response_class= FileResponse, summary="Display user profile picture" )
def get_picture(id: int, db: Session = Depends(get_db) ,current_user: UserBase = Depends(get_current_user)):
    """
        Displays the authenticated user's profile picture based on their username.

        This endpoint returns the profile picture of the currently authenticated user.
        If the user has uploaded a profile picture, the image file will be served as a response.

        If no profile picture is found for the authenticated user, an **HTTP 404** error will be returned.
    """
    db_user.check_current_user(current_user)
    user = get_user_by_id(id, db, current_user)
    if id is not None:
        if not user.profile_picture:
            raise HTTPException(
                status_code=404,
                detail="Profile picture not found for the current user"
            )
        elif id != current_user.id and not current_user.is_admin:
            raise get_admin_exception()
    elif id is None and  not current_user.is_admin:
        raise get_admin_exception()
        
    return user.profile_picture

# @router.delete('/delete/username/{username}',                
#                summary="Delete User by Username")

# def delete_user(username: str, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
#     """
#         Deletes a user from the database based on their unique username. The username is provided as a path parameter. This action is permanent and will remove the user and all associated data from the system.

#         Deletion Requirements:
        
#         1. **Valid Username**: The user with the provided username must exist in the system.

#         Error Handling:
#         - Returns an **HTTP 404** error if the user with the given username does not exist.

#         Upon successful deletion, the user and all associated data are permanently removed from the system, and a confirmation message is returned.
#     """
#     return db_user.delete_user(db, username)

@router.delete('/{id}',
                summary="Delete User by ID" )
def delete_user(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    """
        Deletes a user from the system based on their unique ID. The ID is provided as a path parameter. This action is permanent and will remove the user and all associated data from the system.
        Only a user can delete themselves or the admin.
        Deletion Requirements:
        
        1. **Valid User ID**: The user with the provided ID must exist in the system.
        
        Error Handling:
        - Returns an **HTTP 404** error if the user with the given ID does not exist.
        
        Upon successful deletion, the user and their associated data are permanently removed from the system, and a confirmation message is returned.
    """
    db_user.check_current_user(current_user)

    return db_user.delete_user_by_id(db, id, current_user)

@router.delete(
    "/{id}/profile-picture/",
    summary="Delete a User Profile Picture",
)
def delete_profile_picture(id: int,
    db: Session = Depends(get_db), 
    current_user: UserBase = Depends(get_current_user)
):
    """
        Deletes the profile picture of the currently authenticated user. Only the user or an admin can delete the profile picture.

        This endpoint removes the profile picture file from the server and sets the `profile_picture` field 
        in the database to `None`. If no profile picture exists for the authenticated user, an **HTTP 404** 
        error will be returned.
    """    
    db_user.check_current_user(current_user)
    if id is not None:
        if not current_user.profile_picture:
            raise HTTPException(
                status_code=404,
                detail="No profile picture found for the current user"
            )
        elif id != current_user.id and not current_user.is_admin:
            raise get_admin_exception()
    elif id is None and  not current_user.is_admin:
        raise get_admin_exception()


    profile_picture_path = current_user.profile_picture
    if os.path.exists(profile_picture_path):
        os.remove(profile_picture_path) 
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Profile picture file not found: {profile_picture_path}"
        )


    current_user.profile_picture = None
    db.commit()
    db.refresh(current_user)

    return "Profile picture deleted successfully"