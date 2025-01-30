import asyncio
from json import loads

import aio_pika

from db.rabbitmq import get_rabbitmq
from models.models import Notification
from services.services import send_notification


async def process_message(message: aio_pika.Message):
    async with message.process():
        notification_data = loads(message.body.decode())
        notification = Notification(**notification_data)
        await send_notification(notification)


async def main():
    rabbitmq_connection: aio_pika.Connection = await get_rabbitmq()

    async with rabbitmq_connection:
        channel = await rabbitmq_connection.channel()
        await channel.declare_queue(
            'notification_queue',
            durable=True,
        )
        queue = await channel.get_queue('notification_queue')

        await queue.consume(process_message)

        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
