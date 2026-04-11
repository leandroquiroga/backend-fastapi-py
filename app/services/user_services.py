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
    raise HTTPException(
        status_code=404, detail=f"User {id} not found"
    )  # Devuelve un mensaje si no se encuentra el usuario


def create_user(user: Users) -> Users | None:
    if exist_id(user.id):
        raise HTTPException(status_code=400, detail=f"User already exists")
    users.append(user)
    return user


def update_user(user: Users) -> Users | None:
    # Busca el usuario con el ID especificado y lo actualiza
    for index, saved_user in enumerate(users):
        if saved_user.id == user.id:
            users[index] = user
            return user
    raise HTTPException(status_code=404, detail=f"User {user.id} not found")


def delete_user_id(id: int) -> str:
    # Busca el usuario con el ID especificado y lo elimina
    user = search_user_by_id(id)
    if user:
        users.remove(user)
        return f"User {id} deleted successfully"
    raise HTTPException(status_code=404, detail=f"User {id} not found")
