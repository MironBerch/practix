from os import environ

from pydantic import Field
from pydantic_settings import BaseSettings


class RabbitMQConfig(BaseSettings):
    host: str = environ('RABBITMQ_HOST')
    server_port: int = environ('RABBITMQ_SERVER_PORT')
    client_port: int = environ('RABBITMQ_CLIENT_PORT')
    user: str = environ('RABBITMQ_USER')
    password: str = environ('RABBITMQ_PASS')


class FastAPIConfig(BaseSettings):
    host: str = '0.0.0.0'
    port: int = environ.get('FASTAPI_PORT')
    debug: bool = environ.get('DEBUG') == 'True'


class Settings(BaseSettings):
    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)
    rabbitmq: RabbitMQConfig = Field(default_factory=RabbitMQConfig)


settings = Settings()
