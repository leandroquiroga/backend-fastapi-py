from pydantic import BaseModel, EmailStr, Field

# Entidad Users
class Users(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=50)
    surname: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=20)
    age: int = Field(..., ge=12, le=120)
    
class AuthLogin(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=20)
    full_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    disabled: bool = False