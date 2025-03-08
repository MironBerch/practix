from datetime import datetime

from psycopg2.extensions import connection, cursor

from core.logger import logger
from services.errors import UpdatesNotFoundError


class PostgresExtractor(object):
    """Класс для извлечении данных из `PostgreSQL`."""

    postgres: connection
    table: str

    def __init__(self, postgres: connection, table: str):
        self.postgres = postgres
        self.table = table

    def _select_table(self, timestamp: datetime) -> cursor:
        """Запрашивает обновления в таблице на текущий момент."""
        curs = self.postgres.cursor()
        curs.execute(
            f"""
                SELECT id
                FROM {self.table}
                WHERE created_at > TIMESTAMP '{timestamp}'
                ORDER BY created_at;
            """,
        )
        return curs

    def get_updates(self, timestamp: datetime) -> list[tuple[str, list]]:
        """Извлекает новые данные с момента последнего обновления."""
        curs: cursor = self._select_table(timestamp)
        data = curs.fetchall()
        curs.close()
        if not data:
            raise UpdatesNotFoundError
        logger.info(data)
        return [obj[0] for obj in data]
