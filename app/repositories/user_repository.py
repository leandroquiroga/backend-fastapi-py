from fastapi import HTTPException
from models import UserResponse

users = [
    UserResponse(
        id=1,
        name="Leandro",
        surname="Quiriga",
        email="leandro@example.com",
        username="leandroq",
        age=30,
    ),
    UserResponse(
        id=2,
        name="Maria",
        surname="Gomez",
        email="maria@example.com",
        username="mariag",
        age=25,
    ),
    UserResponse(
        id=3,
        name="Carlos",
        surname="Perez",
        email="carlos@example.com",
        username="carlosp",
        age=28,
    )
]

def search_user(skip: int = 0, limit: int = 10) -> list[UserResponse]:
    # Devuelve una lista de usuarios con paginación
    return users[skip : skip + limit]


def search_user_by_id(id: int) -> UserResponse | None:
    # Busca el usuario con el ID especificado
    user = next((user for user in users if user.id == id), None)
    if user:
        return user  # Devuelve el usuario encontrado
    raise HTTPException(
        status_code=404, detail=f"User {id} not found"
    )  # Devuelve un mensaje si no se encuentra el usuario