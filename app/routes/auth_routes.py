from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from repositories import users_db
from models import LoginRequest
from services import get_current_user, search_user_db

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@auth_router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = next((user for user in users_db if user.username == form.username), None)
    if not user_db:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Incorrect username or disabled user")
      
    user = search_user_db(form.username)
    
    if not user or user.password != form.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
      
    return {"access_token": user.username, "token_type": "bearer"}
  
  
@auth_router.get("/users/me")
async def read_users_me(user: LoginRequest = Depends(get_current_user)):
    return user