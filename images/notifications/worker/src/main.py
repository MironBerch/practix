import asyncio

import aio_pika

from db.rabbitmq import get_rabbitmq


async def process_message(message: aio_pika.Message):
    async with message.process():
        message.body.decode()


async def main():
    rabbitmq_connection: aio_pika.Connection = await get_rabbitmq()

    async with rabbitmq_connection:
        channel = await rabbitmq_connection.channel()
        queue = await channel.get_queue('notification_queue')

        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
