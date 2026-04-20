from fastapi import APIRouter, status
from models import UserResponse, UserCreate, UserDB, UserUpdate
from services import (
    create_user,
    update_user,
    delete_user_id,
)

from repositories import search_user, search_user_by_id

user_router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@user_router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(skip: int = 0, limit: int = 10):
    """Lista todos los usuarios con paginación"""
    users_db = search_user(skip, limit)
    return [UserResponse.model_validate(user.model_dump(by_alias=True)) for user in users_db]


@user_router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: str) -> UserDB:
    """Obtiene un usuario por ID"""
    return search_user_by_id(id)


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def post_create_user(user_data: UserCreate) -> UserResponse:
    """Crea un nuevo usuario (requiere password)"""
    users_db = create_user(user_data)
    return UserResponse.model_validate(users_db.model_dump(by_alias=True))


@user_router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def put_update_user(id: str, user_data: UserUpdate) -> UserResponse:
    """Actualiza un usuario existente (campos opcionales)"""
    updated_user = update_user(id, user_data)
    return UserResponse.model_validate(updated_user.model_dump(by_alias=True))


@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: str) -> dict[str, str]:
    """Elimina un usuario por ID"""
    message = delete_user_id(id)
    return {"message": message}
