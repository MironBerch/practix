import random

from db import redis


def generate_code() -> str:
    return str(random.randint(100000, 999999))


def create_2_step_verification_code(
        email: str,
) -> None:
    redis.redis.set(
        f'2_step_verification_code:{email}',
        generate_code(),
        ex=60*10,
    )


def create_registration_email_verification_code(
        email: str,
) -> None:
    redis.redis.set(
        f'email_registration:{email}',
        generate_code(),
        ex=60*10,
    )


def create_change_email_verification_code(
        old_email: str,
        new_email: str,
) -> None:
    redis.redis.set(
        f'email_change:{old_email}:{new_email}',
        generate_code(),
        ex=60*10,
    )
