from fastapi import HTTPException
from models import User
from typing import List
from utilities.auth_utilities import get_password_hash

# Lista unificada de usuarios (antes había 2: users y users_db)
users: List[User] = [
    User(
        id=1,
        name="Leandro",
        surname="Quiriga",
        email="leandro@example.com",
        username="leandroq",
        age=30,
        password_hash=get_password_hash("password123")
    ),
    User(
        id=2,
        name="Maria",
        surname="Gomez",
        email="maria@example.com",
        username="mariag",
        age=25,
        password_hash=get_password_hash("password456")
    ),
    User(
        id=3,
        name="Carlos",
        surname="Perez",
        email="carlos@example.com",
        username="carlosp",
        age=28,
        password_hash=get_password_hash("password789")
    )
]

def search_user(skip: int = 0, limit: int = 10) -> list[User]:
    """Devuelve una lista de usuarios con paginación"""
    return users[skip : skip + limit]


def search_user_by_id(id: int) -> User:
    """Busca el usuario con el ID especificado"""
    user = next((user for user in users if user.id == id), None)
    if user:
        return user
    raise HTTPException(
        status_code=404, detail=f"User {id} not found"
    )


def search_user_by_username(username: str) -> User | None:
    """Busca usuario por username (para autenticación)"""
    return next((u for u in users if u.username == username), None)