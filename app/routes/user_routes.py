from fastapi import APIRouter, status
from models import UserResponse, UserCreate, User
from services import (
    create_user,
    update_user,
    delete_user_id,
)

from repositories import search_user, search_user_by_id

user_router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@user_router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(skip: int = 0, limit: int = 10) -> list[User]:
    """Lista todos los usuarios con paginación"""
    return search_user(skip, limit)


@user_router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int) -> User:
    """Obtiene un usuario por ID"""
    return search_user_by_id(id)


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def post_create_user(user_data: UserCreate) -> User:
    """Crea un nuevo usuario (requiere password)"""
    return create_user(user_data)


@user_router.put("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def put_update_user(user: User) -> User:
    """Actualiza un usuario existente"""
    return update_user(user)


@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int) -> dict[str, str]:
    """Elimina un usuario por ID"""
    message = delete_user_id(id)
    return {"message": message}
