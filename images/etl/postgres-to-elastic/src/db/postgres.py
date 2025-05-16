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
        'host': environ.get('DB_HOST', 'movies_db'),
        'port': int(environ.get('DB_PORT', 5432)),
        'dbname': environ.get('DB_NAME', 'movies'),
        'user': environ.get('DB_USER', 'postgres'),
        'password': environ.get('DB_PASSWORD', 'postgres'),
        'options': '-c search_path=content',
    }
    connection: postgres_connection = psycopg2.connect(**dsn)
    connection.cursor_factory = DictCursor

    yield connection

    connection.close()
