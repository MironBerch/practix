from os import environ

from redis import Redis


def get_redis() -> Redis:
    return Redis(
        host=environ.get('REDIS_HOST'),
        port=environ.get('REDIS_PORT'),
        db=environ.get('REDIS_DB'),
    )
