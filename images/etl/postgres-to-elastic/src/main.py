import time
from datetime import datetime, timedelta, timezone

from elasticsearch import Elasticsearch
from psycopg2.extensions import connection
from redis import Redis

from core.logger import logger
from db.elastic import get_elastic
from db.postgres import get_postgres
from db.redis import get_redis
from models.genre import Genre
from models.person import Person
from services import extract, load, transform
from services.state import State


def etl_process(
    postgres: extract.PostgresExtractor,
    data: transform.DataTransform,
    elastic: load.ElasticLoader,
    state: State,
) -> None:
    """Запускает внутренние компоненты процесса Extract-Transform-Load."""
    timestamp = state.get('last_updated', datetime.min)
    for table, rows in postgres.get_updates(timestamp):
        if table == 'genre':
            elastic.bulk_insert(data=[Genre(**row) for row in rows])
        if table == 'person':
            elastic.bulk_insert(data=[Person(**row) for row in rows])
        for film_work_id in postgres.get_film_work_ids(table, rows):
            data.add_film_work_id(film_work_id)
    elastic.bulk_insert(
        data.transform_film_works(
            postgres.get_film_works_data(data.get_film_work_ids()),
        ),
    )


def postgres_to_elastic(postgres: connection, elastic: Elasticsearch, redis: Redis) -> None:
    state = State(redis)
    while True:
        try:
            etl_process(
                extract.PostgresExtractor(postgres),
                transform.DataTransform(redis),
                load.ElasticLoader(elastic),
                state,
            )
        except extract.UpdatesNotFoundError:
            logger.info('Нет обновлений')
        else:
            logger.info('Есть обновления')
            state.set(
                'last_updated',
                datetime.now(tz=timezone(timedelta(hours=3))).strftime('%Y-%m-%dT%H:%M:%S'),
            )
        finally:
            logger.info('Повторный запрос через 1 минуту.')
        time.sleep(60)


def main() -> None:
    with get_postgres() as postgres_connection:
        with get_redis() as redis_connection:
            with get_elastic() as elastic_connection:
                postgres_to_elastic(
                    postgres_connection,
                    elastic_connection,
                    redis_connection,
                )


if __name__ == '__main__':
    main()
