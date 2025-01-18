from os import environ

from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    host: str = environ.get('POSTGRES_HOST')
    port: int = int(environ.get('POSTGRES_PORT'))
    db: str = environ.get('POSTGRES_NAME')
    user: str = environ.get('POSTGRES_USER')
    password: str = environ.get('POSTGRES_PASSWORD')


class RabbitMQConfig(BaseSettings):
    host: str = environ.get('RABBITMQ_HOST')
    server_port: int = environ.get('RABBITMQ_SERVER_PORT')
    client_port: int = environ.get('RABBITMQ_CLIENT_PORT')
    user: str = environ.get('RABBITMQ_USER')
    password: str = environ.get('RABBITMQ_PASS')


class FastAPIConfig(BaseSettings):
    host: str = '0.0.0.0'
    port: int = environ.get('FASTAPI_PORT')
    debug: bool = environ.get('DEBUG') == 'True'


class Settings(BaseSettings):
    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)
    rabbitmq: RabbitMQConfig = Field(default_factory=RabbitMQConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)


settings = Settings()
