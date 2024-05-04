from datetime import timedelta
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from core.meds import FindPharmacy
from models.auth import Token
from models.auth import UserCreate
from core.auth import create_user
from core.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    User,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)

router = APIRouter(prefix="/auth")

@router.post("/signup")
async def create_user_account(user: UserCreate):
    created_user = await create_user(user.username, user.password, user.email, user.full_name)
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Username already exists",
        )
    return created_user

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/pharmacy")
async def pharmacy(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    pharmacy=await FindPharmacy(current_user.username)
    if pharmacy:
        return pharmacy
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No Pharmacy Found",
        )

@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
