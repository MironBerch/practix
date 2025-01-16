import aio_pika

rabbitmq: aio_pika.Connection | None = None


async def get_rabbitmq():
    return rabbitmq
