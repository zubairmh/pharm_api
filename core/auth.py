from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.database import users
from models.auth import TokenData, User, UserInDB
import os
from dotenv import load_dotenv

load_dotenv()
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


users_collection = users


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    user = await users_collection.find_one({"username": username})
    if user:
        del user["_id"]
        return UserInDB(**user)

async def create_user(username: str, password: str, email: str, full_name: str):
    user=await get_user(username)
    if user:
        return False
    user={"username":username,"email":email,"full_name":full_name,"hashed_password":get_password_hash(password),"disabled":False}
    await users_collection.insert_one(user)
    return True

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

 
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
 