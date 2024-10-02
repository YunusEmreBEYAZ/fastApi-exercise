from fastapi import APIRouter, Depends
from fastapi import Request
from pydantic import BaseModel

router = APIRouter(
    prefix = "/dependencies",
    tags= ["dependencies"]
)

def convert_headers(request: Request):
    new_headers = []
    for key, value in request.headers.items():
        new_headers.append(f"{key} -*- {value}")
    return new_headers

@router.get("/")
def get_headers(headers= Depends(convert_headers)):
    return headers


class Account(BaseModel):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

@router.post("/account")
def create_account(account: Account = Depends()):
    return {
        "name": account.name,
        "email": account.email
    }



