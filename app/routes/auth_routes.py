from fastapi import APIRouter, Depends
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from services import authenticate_user, get_current_user
from utilities import create_access_token
from models import UserResponse

ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@auth_router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()) -> dict[str, bytes | str]:
    user = authenticate_user(form.username, form.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me")
async def read_users_me(user: UserResponse = Depends(get_current_user)):
    return user
