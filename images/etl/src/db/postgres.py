from contextlib import contextmanager
from os import environ
from typing import Iterator

import psycopg2
from psycopg2.extensions import connection as postgres_connection
from psycopg2.extras import DictCursor


@contextmanager
def get_postgres() -> Iterator[postgres_connection]:
    """
    Функция с контекстным менеджером для подключении к базе данных PostgreSQL.
    """

    dsn: dict[str, str | int] = {
        'dbname': environ.get('DB_NAME'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD'),
        'host': environ.get('DB_HOST'),
        'port': int(environ.get('DB_PORT')),
        'options': '-c search_path=content',
    }
    connection: postgres_connection = psycopg2.connect(**dsn)
    connection.cursor_factory = DictCursor

    yield connection

    connection.close()
