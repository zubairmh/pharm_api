from fastapi import APIRouter
from pydantic import BaseModel

router=APIRouter("/auth")

class Location(BaseModel):
    long: float
    lat: float

class LoginModel(BaseModel):
    user: str
    password: str
    location: Location


class LoginResponse(BaseModel):
    auth_token: str
    refresh_token: str


@router.post("/login")
async def login(data: LoginModel) -> LoginResponse:
    return LoginResponse(
        auth_token="abcd",
        refresh_token="abcd"
    )
