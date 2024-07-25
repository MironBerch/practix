from typing import Any

from redis import Redis

redis: Redis | None = None


class RedisAdapter:
    def __init__(self, redis_instance: Redis):
        self.redis = redis_instance

    async def get_objects_from_cache(self, redis_key: str) -> Any:
        data = await self.redis.get(redis_key)
        if not data:
            return None
        return data

    async def put_objects_to_cache(
            self,
            redis_key: str,
            objects: list | dict,
            expire: int = 60 * 10,
    ) -> None:
        await self.redis.set(redis_key, objects, ex=expire)


async def get_redis() -> RedisAdapter:
    return RedisAdapter(redis_instance=redis)
