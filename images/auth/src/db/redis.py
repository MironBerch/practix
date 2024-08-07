from redis import Redis

from core.config import settings

redis: Redis | None = None


def init():
    return Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
        decode_responses=True,
    )


def get_redis() -> Redis:
    return redis
