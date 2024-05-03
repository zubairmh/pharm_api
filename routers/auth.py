from fastapi import APIRouter
from pydantic import BaseModel
import uuid
router=APIRouter(prefix="/auth")

# Login Models
class Location(BaseModel):
    long: float
    lat: float

class LoginModel(BaseModel):
    user: str
    password: str
    location: Location

class RegisterModel(BaseModel):
    user: str
    password: str

class LoginResponse(BaseModel):
    auth_token: str

class RegisterResponse(BaseModel):
    status: bool


# Login Routes
@router.post("/login")
async def login(data: LoginModel) -> LoginResponse:
    return LoginResponse(
        auth_token=str(uuid.uuid4()),
    )


@router.post("/register")
async def register(data: RegisterModel) -> RegisterResponse:
    return RegisterResponse(
        status=True
    )

