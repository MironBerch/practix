from os import environ

from pydantic import Field
from pydantic_settings import BaseSettings


class FastAPIConfig(BaseSettings):
    host: str = '0.0.0.0'
    port: int = environ.get('FASTAPI_PORT')
    debug: bool = environ.get('DEBUG') == 'True'


class MongoConfig(BaseSettings):
    host: str = 'mongo'
    port: int = environ.get('MONGO_PORT')
    db: str = 'default'


class Settings(BaseSettings):
    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)
    mongo: MongoConfig = Field(default_factory=MongoConfig)


settings = Settings()
