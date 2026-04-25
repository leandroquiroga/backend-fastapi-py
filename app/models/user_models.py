from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from datetime import datetime
from utilities import utc_now
from enum import Enum

# Helper para manejar ObjectId de MongoDB
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler): # type: ignore
        from pydantic_core import core_schema
        
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate), # type: ignore
            ])
        ],
        serialization=core_schema.plain_serializer_function_ser_schema(
            lambda x: str(x)
        ))
        
    @classmethod
    def validate(cls, v): # type: ignore
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if ObjectId.is_valid(v):
                return ObjectId(v)
        raise ValueError("Invalid ObjectId")


class UserRole(str, Enum):
  """Roles de usuario para control de acceso"""
  ADMIN = "admin"
  USER = "user"
  GUEST = "guest"
  

# Modelos de usuario 
class UserDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., min_length=3, max_length=50)
    surname: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=20)
    age: int = Field(..., ge=12, le=120)
    password_hash: str
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    role: UserRole = Field(default=UserRole.USER)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Entidad Users
class UserCreate(BaseModel):
  """DTO para registro de usuario (POST /register)"""
  name: str = Field(..., min_length=3, max_length=50)
  surname: str = Field(..., min_length=3, max_length=50)
  email: EmailStr
  username: str = Field(..., min_length=3, max_length=20)
  age: int = Field(..., ge=12, le=120)
  password: str = Field(..., min_length=6, max_length=16)
  role: UserRole = Field(default=UserRole.USER)


class LoginRequest(BaseModel):
  """DTO para login (POST /login)"""
  username: str = Field(..., min_length=3, max_length=20)
  password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
  """DTO para actualizar usuario (PUT /users/{id}) - campos opcionales"""
  name: str | None = Field(None, min_length=3, max_length=50)
  surname: str | None = Field(None, min_length=3, max_length=50)
  email: EmailStr | None = None
  username: str | None = Field(None, min_length=3, max_length=20)
  age: int | None = Field(None, ge=12, le=120)


class UserResponse(BaseModel):
  """DTO para respuestas GET - sin datos sensibles"""
  id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
  name: str
  surname: str
  email: EmailStr
  username: str
  age: int
  role: UserRole = Field(default=UserRole.USER)
  class Config:
    from_attributes = True
    populate_by_name = True
    json_encoders = {ObjectId: str}


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