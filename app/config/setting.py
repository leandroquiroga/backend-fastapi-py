import os
from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    """Función auxiliar para obtener variables de entorno y lanzar error si no están definidas."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is not set in the environment variables.")
    return value


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = _require_env("SECRET_KEY")
ALGORITHM = _require_env("ALGORITHM")
URL_MONGO_DB = _require_env("URL_MONGO_DB")
DATABASE_NAME = _require_env("DATABASE_NAME")
REDIS_CACHE_HOST = _require_env("REDIS_HOST")
REDIS_CACHE_PORT = _require_env("REDIS_PORT")
REDIS_CACHE_DB = _require_env("REDIS_DB")
CACHE_TTL_USER = _require_env("CACHE_TTL_USER")
CACHE_TTL_LOGIN = _require_env("CACHE_TTL_LOGIN")
CACHE_TTL_USERS_LIST = _require_env("CACHE_TTL_USERS_LIST")
