from datetime import datetime
from typing import Iterator

from psycopg2.extensions import connection, cursor
from psycopg2.extras import DictRow

from services.errors import UpdatesNotFoundError


class PostgresExtractor(object):
    """Класс для извлечении данных из `PostgreSQL`."""

    postgres: connection

    TABLES = ('film_work', 'person', 'genre')

    def __init__(self, postgres: connection):
        self.postgres = postgres

    def _select_table(self, table: str, timestamp: datetime) -> cursor:
        """Запрашивает обновления в таблице на текущий момент."""
        curs = self.postgres.cursor()
        curs.execute(
            f"""
                SELECT *
                FROM {table}
                WHERE updated_at > TIMESTAMP '{timestamp}'
                ORDER BY updated_at;
            """,
        )
        return curs

    def get_updates(self, timestamp: datetime) -> Iterator[tuple[str, list]]:
        """Извлекает новые данные с момента последнего обновления."""
        updates = {table: self._select_table(table, timestamp) for table in self.TABLES}
        if not any(curs.rowcount for curs in updates.values()):
            raise UpdatesNotFoundError
        for table, curs in updates.items():
            data = curs.fetchall()
            if data:
                yield (table, data)
            curs.close()

    def get_film_work_ids(self, table: str, data: list[DictRow]) -> list[str]:
        """Извлекает id фильмов, в которых произошли изменения."""
        if table in {'person', 'genre'}:
            with self.postgres.cursor() as curs:
                film_work_ids = ', '.join([f"'{row['id']}'" for row in data])
                curs.execute(
                    f"""
                        SELECT film_work.id
                        FROM film_work
                        LEFT JOIN {table}_film_work gpfw ON gpfw.film_work_id = film_work.id
                        WHERE gpfw.{table}_id IN ({film_work_ids})
                        ORDER BY film_work.updated_at;
                    """,
                )
                return [row['id'] for row in curs.fetchall()]
        else:
            return [row['id'] for row in data]

    def get_film_works_data(self, film_work_ids: list[str]) -> Iterator[DictRow]:
        with self.postgres.cursor() as cursor:
            film_work_ids = ', '.join([f"'{film_work_id}'" for film_work_id in film_work_ids])
            cursor.execute(
                f"""
                    SELECT
                        film_work.id,
                        film_work.title,
                        film_work.description,
                        film_work.rating,
                        person_film_work.role as person_roles,
                        person.id as person_ids,
                        person.full_name as person_names,
                        genre.name as genre_names
                    FROM film_work
                    LEFT JOIN person_film_work ON person_film_work.film_work_id = film_work.id
                    LEFT JOIN person ON person.id = person_film_work.person_id
                    LEFT JOIN genre_film_work ON genre_film_work.film_work_id = film_work.id
                    LEFT JOIN genre ON genre.id = genre_film_work.genre_id
                    WHERE film_work.id IN ({film_work_ids})
                """,
            )
            return cursor.fetchall()
