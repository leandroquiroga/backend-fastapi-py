import jwt as pyjwt
from fastapi import HTTPException, status, Depends
from utilities import oauth2, verify_password
from models import User
from repositories import search_user_by_username,search_user_by_user_name_response
from config import SECRET_KEY, ALGORITHM

async def get_current_user(token: str = Depends(oauth2)):
    """ Esta función se puede implementar para obtener el usuario actual a partir del token de autenticación."""
    
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found in token")
        
    except pyjwt.ExpiredSignatureError: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = search_user_by_user_name_response(username)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
      
    return user
  
def authenticate_user(username: str, password: str) -> User:
    """Esta función se puede implementar para autenticar al usuario utilizando el token"""
    user = search_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password has not been verified")
    
    return user