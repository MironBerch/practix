from typing import Any

from redis import Redis


class State(object):
    """Класс для хранения состояния при работе с данными."""

    redis: Redis

    def __init__(self, redis) -> None:
        self.redis = redis

    def set(self, key: str, value: Any) -> None:
        self.redis.set(key, value)

    def get(self, key: str, default: Any = None) -> Any:
        value = self.redis.get(key)
        if not value:
            return default
        return self.redis.get(key)
