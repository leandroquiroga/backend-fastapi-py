from fastapi import APIRouter, HTTPException, Depends, status
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from repositories import users_db
from utilities import create_access_token, verify_password
from services import search_user_db

ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@auth_router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()) -> dict[str, bytes | str]:
    user_db = next((user for user in users_db if user.username == form.username), None)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = search_user_db(form.username)

    if not user or not verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @auth_router.get("/users/me")
# async def read_users_me(user: LoginRequest = Depends(get_current_user)):
#     return user
