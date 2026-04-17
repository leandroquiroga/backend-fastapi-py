from pydantic import BaseModel, EmailStr, Field

# Entidad Users
class UserCreate(BaseModel):
  """DTO para registro de usuario (POST /register)"""
  name: str = Field(..., min_length=3, max_length=50)
  surname: str = Field(..., min_length=3, max_length=50)
  email: EmailStr
  username: str = Field(..., min_length=3, max_length=20)
  age: int = Field(..., ge=12, le=120)
  password: str = Field(..., min_length=6, max_length=16)


class LoginRequest(BaseModel):
  """DTO para login (POST /login)"""
  username: str = Field(..., min_length=3, max_length=20)
  password: str = Field(..., min_length=6, max_length=100)


class UserResponse(BaseModel):
  """DTO para respuestas GET - sin datos sensibles"""
  id: int
  name: str
  surname: str
  email: EmailStr
  username: str
  age: int

  class Config:
    from_attributes = True


class User(BaseModel):
  """Modelo principal interno - con password_hash"""
  id: int
  name: str
  surname: str
  email: EmailStr
  username: str
  age: int
  password_hash: str

  class Config:
    from_attributes = True
    
class AuthToken(BaseModel):
  """DTO para respuesta de token JWT"""
  access_token: str
  token_type: str = "bearer"