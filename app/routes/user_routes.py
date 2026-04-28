from fastapi import APIRouter, status, Depends, HTTPException
from models import UserResponse, UserCreate, UserDB, UserUpdate, ChangePasswordRequest
from services import create_user, delete_user_id, update_user

from repositories import search_user, search_user_by_id, change_user_password
from utilities import (
    require_rol,
    change_password_rate_limiter,
    get_user_rate_limiter,
    get_users_rate_limiter,
    update_user_rate_limiter,
    cache_get_user,
    cache_set_user,
)

user_router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@user_router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    skip: int = 0,
    limit: int = 10,
    current_user=Depends(require_rol(["admin", "user"])),
    _: None = Depends(get_users_rate_limiter),
):
    """Lista todos los usuarios con paginación"""
    users_db = search_user(skip, limit)

    if current_user.role != "admin":
        users_db = [user for user in users_db if user.role != "admin"]
    return [
        UserResponse.model_validate(user.model_dump(by_alias=True)) for user in users_db
    ]


@user_router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    id: str,
    current_user=Depends(require_rol(["admin", "user"])),
    _: None = Depends(get_user_rate_limiter),
) -> UserDB:
    """Obtiene un usuario por ID (solo tu perfil o admin puede ver cualquiera)"""
    cached_user = cache_get_user(id)
    if cached_user:
        user = UserDB(**cached_user)

    else:
        user = search_user_by_id(id)
        cache_set_user(id, user.model_dump(by_alias=True, mode="json"))

    if current_user.role != "admin":
        # Bloquear ver usuarios admin
        if user.role == "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        # Bloquear ver otros usuarios normales (solo tu perfil)
        if str(user.id) != str(current_user.id):
            raise HTTPException(
                status_code=403, detail="You can only view your own profile"
            )

    return UserResponse.model_validate(user.model_dump(by_alias=True, mode="json"))


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def post_create_user(
    user_data: UserCreate, current_user=Depends(require_rol(["admin"]))
) -> UserResponse:
    """Crea un nuevo usuario (requiere password)"""
    users_db = create_user(user_data)
    return UserResponse.model_validate(users_db.model_dump(by_alias=True))


@user_router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    data: ChangePasswordRequest,
    current_user=Depends(require_rol(["admin", "user"])),
    _: None = Depends(change_password_rate_limiter),
):
    """Cambia la contraseña del usuario autenticado (siempre tu propia contraseña)"""
    message = change_user_password(str(current_user.id), data)
    return {"message": message}


@user_router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def put_update_user(
    id: str,
    user_data: UserUpdate,
    current_user=Depends(require_rol(["admin", "user"])),
    _: None = Depends(update_user_rate_limiter),
) -> UserResponse:
    """Actualiza un usuario existente (solo tu perfil o admin puede actualizar cualquiera)"""

    if current_user.role != "admin" and str(current_user.id) != id:
        raise HTTPException(
            status_code=403, detail="You can only update your own profile"
        )

    updated_user = update_user(id, user_data)
    return UserResponse.model_validate(updated_user.model_dump(by_alias=True))


@user_router.delete("/{id}")
async def delete_user(id: str, user=Depends(require_rol(["admin"]))) -> dict[str, str]:
    """Elimina un usuario por ID"""
    message = delete_user_id(id)
    return {"message": message}
