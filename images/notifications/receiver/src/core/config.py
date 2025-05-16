from os import environ

from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    host: str = environ.get('POSTGRES_HOST', 'notifications_db')
    port: int = int(environ.get('POSTGRES_PORT', 5432))
    db: str = environ.get('POSTGRES_NAME', 'notifications')
    user: str = environ.get('POSTGRES_USER', 'postgres')
    password: str = environ.get('POSTGRES_PASSWORD', 'postgres')


class RabbitMQConfig(BaseSettings):
    host: str = environ.get('RABBITMQ_HOST', 'rabbit')
    server_port: int = int(environ.get('RABBITMQ_SERVER_PORT', 15672))
    client_port: int = int(environ.get('RABBITMQ_CLIENT_PORT', 5672))
    user: str = environ.get('RABBITMQ_USER', 'user')
    password: str = environ.get('RABBITMQ_PASS', 'password')


class FastAPIConfig(BaseSettings):
    host: str = '0.0.0.0'
    port: int = int(environ.get('FASTAPI_PORT', 8000))
    debug: bool = environ.get('DEBUG') == 'True'


class Settings(BaseSettings):
    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)
    rabbitmq: RabbitMQConfig = Field(default_factory=RabbitMQConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)


settings = Settings()
