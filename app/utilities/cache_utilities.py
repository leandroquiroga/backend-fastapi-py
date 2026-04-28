import json
from config import redis_client, CACHE_TTL_USER


def cache_get_user(key: str):
    """Obtener valor del cache"""
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def cache_set_user(key: str, value: dict | str):
    """Establecer valor en el cache"""
    redis_client.setex(key, int(CACHE_TTL_USER), json.dumps(value))


def cache_delete_user(key: str):
    """Eliminar valor del cache"""
    redis_client.delete(key)


def cache_clear_all():
    """Limpiar todo el cache (para pruebas)"""
    redis_client.flushdb()
