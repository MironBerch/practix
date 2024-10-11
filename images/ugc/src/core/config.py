from os import environ

from pydantic import Field
from pydantic_settings import BaseSettings


class FastAPIConfig(BaseSettings):
    host: str = '0.0.0.0'
    port: int = environ.get('FASTAPI_PORT')
    secret_key: str = environ.get('SECRET_KEY')
    debug: bool = environ.get('DEBUG') == 'True'


class Settings(BaseSettings):
    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)


settings = Settings()
