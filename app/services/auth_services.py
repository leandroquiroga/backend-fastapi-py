from fastapi import HTTPException, status, Depends
from utilities import oauth2
from models import LoginRequest
from repositories import users_db

def search_user_db(username: str) -> LoginRequest | None:
    # Busca el usuario con el username especificado
    for user in users_db:
        if user.username == username:
            return user
    return None

async def get_current_user(token: str = Depends(oauth2)):
    user = search_user_db(token)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
      
    return user