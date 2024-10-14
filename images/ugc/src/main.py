from contextlib import asynccontextmanager
from logging import DEBUG

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from db import mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo.start()

    yield

    await mongo.stop()


app = FastAPI(
    title='Movies UGC v1',
    description='Movies UGC',
    version='1.0',
    docs_url='/movie/api/v1/docs',
    openapi_url='/movie/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=settings.fastapi.host,
        port=settings.fastapi.port,
        log_level=DEBUG,
        reload=True,
    )
