from contextlib import asynccontextmanager
from logging import DEBUG

import aio_pika
import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.urls import api_router
from core.config import settings
from core.logger import LOGGING
from db import rabbitmq


@asynccontextmanager
async def lifespan(app: FastAPI):
    user = settings.rabbitmq.user
    password = settings.rabbitmq.password
    host = settings.rabbitmq.host
    port = settings.rabbitmq.client_port

    rabbitmq.rabbitmq = await aio_pika.connect_robust(f'amqp://{user}:{password}@{host}:{port}')

    async with rabbitmq.rabbitmq.channel() as channel:
        await channel.declare_queue(
            'notification_queue',
            durable=True,
        )

    yield

    await rabbitmq.rabbitmq.close()


app = FastAPI(
    title='Notifications reciver API v1',
    description='Notifications reciver API',
    version='1.0',
    docs_url='/notifications/api/docs',
    openapi_url='/notifications/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(api_router, prefix='/notifications')


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=settings.fastapi.host,
        port=settings.fastapi.port,
        log_config=LOGGING,
        log_level=DEBUG,
        reload=True,
    )
