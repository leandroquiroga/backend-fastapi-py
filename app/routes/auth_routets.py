from fastapi import APIRouter
from models import AuthLogin # type: ignore

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])