import redis
from config.setting import (
    REDIS_CACHE_DB,
    REDIS_CACHE_HOST,
    REDIS_CACHE_PORT,
)

redis_client = redis.Redis(
    host=REDIS_CACHE_HOST,
    port=int(REDIS_CACHE_PORT),
    db=int(REDIS_CACHE_DB),
    decode_responses=True
)