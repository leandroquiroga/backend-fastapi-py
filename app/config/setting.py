import os
from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    """ Función auxiliar para obtener variables de entorno y lanzar error si no están definidas. """
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is not set in the environment variables.")
    return value


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = _require_env("SECRET_KEY")
ALGORITHM = _require_env("ALGORITHM")