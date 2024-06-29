from __future__ import annotations

import logging
import sqlite3
from os import environ
from typing import TYPE_CHECKING

import psycopg2
from psycopg2._psycopg import connection as postgres_connection_object
from psycopg2.extras import DictCursor, execute_values
from schemas import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork, schemas

if TYPE_CHECKING:
    SQL = str
    from schemas import Schema

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict:
    d = {}
    for index, column in enumerate(cursor.description):
        d[column[0]] = row[index]
    return d


def parse_db_field_names(db_field_names: tuple[str]) -> str:
    return ', '.join(db_field_names)


class DataExtraction:
    def __init__(self, sqlite_connection: sqlite3.Connection):
        self.sqlite_connection = sqlite_connection
        self.sqlite_connection.row_factory = dict_factory

    def extract_data(self) -> dict[str, list[Schema]]:
        cursor = self.sqlite_connection.cursor()
        cursor.execute("""SELECT * FROM film_work;""")
        film_works = [
            Filmwork(**film_work) for film_work in cursor.fetchall()
        ]
        cursor.execute("""SELECT * FROM genre;""")
        genres = [
            Genre(**genre) for genre in cursor.fetchall()
        ]
        cursor.execute("""SELECT * FROM person;""")
        persons = [
            Person(**person) for person in cursor.fetchall()
        ]
        cursor.execute("""SELECT * FROM genre_film_work;""")
        genre_film_work = [
            GenreFilmwork(**genre_film_work) for genre_film_work in cursor.fetchall()
        ]
        cursor.execute("""SELECT * FROM person_film_work;""")
        person_film_works = [
            PersonFilmwork(**person_film_work) for person_film_work in cursor.fetchall()
        ]
        return {
            'film_works': film_works,
            'genres': genres,
            'persons': persons,
            'genre_film_work': genre_film_work,
            'person_film_works': person_film_works,
        }


class PostgresDataLoader:
    def __init__(self, postgres_connection: postgres_connection_object):
        self.postgres_connection = postgres_connection

    def load_data(self, data: dict[str, list[Schema]]):
        with self.postgres_connection.cursor() as cursor:
            for schema, objects in data.items():
                db_table_name = schemas[schema].db_table_name()
                db_field_names = schemas[schema].get_db_field_names()
                sql = f"""
                    INSERT INTO {db_table_name}
                    ({parse_db_field_names(db_field_names)})
                    VALUES %s
                    ON CONFLICT (id) DO NOTHING
                """
                try:
                    execute_values(
                        cursor,
                        sql,
                        [obj.to_tuple() for obj in objects],
                    )
                    logging.info(
                        f'Сохраняем данные в postgres, таблица: '
                        f'{db_table_name}',
                    )
                except psycopg2.OperationalError as e:
                    logging.error(f'psycopg2 operational error: `{e}`')
                    cursor.close()
                    raise


def load_from_sqlite(
    sqlite_connection: sqlite3.Connection,
    postgres_connection: postgres_connection_object,
):
    logging.info('Начато извлечение данных из  и загрузка в PostgreSQL')

    sqlite_data_extraction = DataExtraction(sqlite_connection)
    postgres_data_loader = PostgresDataLoader(postgres_connection)

    data = sqlite_data_extraction.extract_data()
    postgres_data_loader.load_data(data)


if __name__ == '__main__':
    dsn: dict[str, str | int] = {
        'dbname': environ.get('DB_NAME'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD'),
        'host': environ.get('DB_HOST'),
        'port': int(environ.get('DB_PORT')),
    }
    with sqlite3.connect('db.sqlite') as sqlite_connection, \
            psycopg2.connect(**dsn, cursor_factory=DictCursor) as postgres_connection:
        load_from_sqlite(
            sqlite_connection=sqlite_connection,
            postgres_connection=postgres_connection,
        )
