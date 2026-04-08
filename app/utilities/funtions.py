from fastapi import HTTPException
from models.user_models import users, Users
from utilities.validation import exist_id


def search_user(skip: int = 0, limit: int = 10) -> list[Users]:
    # Devuelve una lista de usuarios con paginación
    return users[skip : skip + limit]
    

def search_user_by_id(id: int) -> Users | None:
    # Busca el usuario con el ID especificado
    user = next((user for user in users if user.id == id), None)
    if user: 
        return user  # Devuelve el usuario encontrado
    raise HTTPException(status_code=404, detail=f"User {id} not found")  # Devuelve un mensaje si no se encuentra el usuario
  
  
def create_user(user: Users) -> Users | None:
  if exist_id(user.id):
    raise HTTPException(status_code=400, detail=f"User {user.id} already exists")
  users.append(user)
  return user