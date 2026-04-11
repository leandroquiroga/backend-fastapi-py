from fastapi import HTTPException
from repositories import users, search_user_by_id
from models import Users
from utilities import exist_id


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
