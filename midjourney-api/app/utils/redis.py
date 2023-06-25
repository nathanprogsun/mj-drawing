import redis
from app.config import settings


def setup_redis():
    return redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)


redis_client = setup_redis()
