import jwt as pyjwt
from fastapi import HTTPException, status, Depends
from utilities import oauth2, verify_password
from models import User
from repositories import search_user_by_username
from config import SECRET_KEY, ALGORITHM

async def get_current_user(token: str = Depends(oauth2)):
    """ Esta función se puede implementar para obtener el usuario actual a partir del token de autenticación."""
    
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        
    except pyjwt.ExpiredSignatureError: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = search_user_by_username(username)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
      
    return user
  
def authenticate_user(username: str, password: str) -> User:
    """Esta función se puede implementar para autenticar al usuario utilizando el token"""
    user = search_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    return user