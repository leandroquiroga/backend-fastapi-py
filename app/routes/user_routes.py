from fastapi import APIRouter
from models.user_models import Users
from utilities.funtions import search_user_by_id, search_user, create_user


router = APIRouter()

@router.get("/users")
async def get_users(skip: int = 0, limit: int = 10) -> list[Users]:
  return search_user(skip, limit)


@router.get("/user/{id}")
async def get_user_by_id(id: int) -> Users | None:
  return search_user_by_id(id)


@router.post("/user")
async def post_create_user(user: Users) -> Users | None:
  return create_user(user)