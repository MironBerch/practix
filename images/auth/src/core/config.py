from os import environ

from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    host: str = environ.get('DB_HOST')
    port: int = int(environ.get('DB_PORT'))
    db: str = environ.get('DB_NAME')
    user: str = environ.get('DB_USER')
    password: str = environ.get('DB_PASSWORD')


class RedisConfig(BaseSettings):
    host: str = environ.get('REDIS_HOST')
    port: int = int(environ.get('REDIS_PORT'))
    db: int = int(environ.get('REDIS_DB'))


class FlaskConfig(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 5000
    secret_key: str = environ.get('SECRET_KEY')
    debug: bool = environ.get('DEBUG') == 'True'


class Settings(BaseSettings):
    flask: FlaskConfig = Field(default_factory=FlaskConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)


settings = Settings()