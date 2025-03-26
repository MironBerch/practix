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
    port: int = int(environ.get('FLASK_PORT'))
    secret_key: str = environ.get('SECRET_KEY')
    debug: bool = environ.get('DEBUG') == 'True'


class SecurityConfig(BaseSettings):
    jwt_secret_key: str = environ.get('JWT_SECRET_KEY')
    jwt_temp_token_expires: int = 60 * 60
    jwt_access_token_expires: int = 24 * 60 * 60
    jwt_refresh_token_expires: int = 30 * 24 * 60 * 60


class NotificationsConfig(BaseSettings):
    receiver_host: str = environ.get('NOTIFICATIONS_RECEIVER_HOST')
    receiver_port: int = environ.get('NOTIFICATIONS_RECEIVER_PORT')


class Settings(BaseSettings):
    flask: FlaskConfig = Field(default_factory=FlaskConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    notifications: NotificationsConfig = Field(default_factory=NotificationsConfig)


settings = Settings()
