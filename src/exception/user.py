from fastapi import HTTPException, status


def get_credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )

def get_admin_exception():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Only admins can perfom this action."
    )