from os import environ

import aio_pika


async def get_rabbitmq() -> aio_pika.Connection:
    host: str = environ.get('RABBITMQ_HOST')
    client_port: int = int(environ.get('RABBITMQ_CLIENT_PORT'))
    user: str = environ.get('RABBITMQ_USER')
    password: str = environ.get('RABBITMQ_PASS')

    rabbitmq: aio_pika.Connection | None = None

    rabbitmq = await aio_pika.connect_robust(f'amqp://{user}:{password}@{host}:{client_port}')

    return rabbitmq
