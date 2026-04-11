from pydantic import BaseModel

# Entidad Users
class Users(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    username: str
    age: int
