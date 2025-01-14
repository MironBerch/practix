from logging import DEBUG

import uvicorn
from core.config import settings
from core.logger import LOGGING

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title='Notifications reciver API v1',
    description='Notifications reciver API',
    version='1.0',
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        log_config=LOGGING,
        log_level=DEBUG,
        reload=True,
    )
