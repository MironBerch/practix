import random

from src.db.redis import RedisAdapter


async def create_2_step_verification_code(email: str, redis_adapter: RedisAdapter) -> str:
    code = str(random.randint(100000, 999999))
    await redis_adapter.put_object_to_cache(
        f'2_step_verification_code:{email}',
        code,
        ex=60 * 10,
    )
    return code


async def create_registration_email_verification_code(
    email: str, redis_adapter: RedisAdapter
) -> str:
    code = str(random.randint(100000, 999999))
    await redis_adapter.put_object_to_cache(
        f'email_registration:{email}',
        code,
        ex=60 * 10,
    )
    return code


async def create_change_email_verification_code(
    old_email: str,
    new_email: str,
    redis_adapter: RedisAdapter,
) -> str:
    code = str(random.randint(100000, 999999))
    await redis_adapter.put_object_to_cache(
        f'email_change:{old_email}',
        new_email + ':' + code,
        ex=60 * 10,
    )
    return code
