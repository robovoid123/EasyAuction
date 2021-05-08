import redis

from app.core.config import settings

redis = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT)
