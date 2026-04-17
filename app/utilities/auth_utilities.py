import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from typing import Dict, Any

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# Instancia de PasswordHash para el manejo de contraseñas.
password_hash = PasswordHash.recommended()

# Instancia de OAuth2PasswordBearer para la autenticacion.
oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Funcion para verificar la contraseña"""
    return password_hash.verify(plain_password, hashed_password)
  
def get_password_hash(password: str) -> str:
    """Funcion para hashear la contraseña"""
    return password_hash.hash(password)
  
def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None):
    """Funcion para crear un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    to_encode.update({"exp": int(expire.timestamp())})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt