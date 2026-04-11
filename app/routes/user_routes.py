from fastapi import APIRouter, status
from models import Users
from services import (
    create_user,
    update_user,
    delete_user_id,
)

from repositories import search_user, search_user_by_id

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/", response_model=list[Users], status_code=status.HTTP_200_OK)
async def get_users(skip: int = 0, limit: int = 10) -> list[Users]:
    return search_user(skip, limit)


@router.get("/{id}", response_model=Users, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int) -> Users | None:
    return search_user_by_id(id)


@router.post("/", response_model=Users, status_code=status.HTTP_201_CREATED)
async def post_create_user(user: Users) -> Users | None:
    return create_user(user)


@router.put("/", response_model=Users, status_code=status.HTTP_200_OK)
async def put_update_user(user: Users) -> Users | None:
    return update_user(user)


@router.delete("/{id}", response_model=str, status_code=status.HTTP_200_OK)
async def delete_user(id: int) -> str:
    return delete_user_id(id)
