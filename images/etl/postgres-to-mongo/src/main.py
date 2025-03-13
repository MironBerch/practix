import time
from datetime import datetime, timedelta, timezone
from uuid import UUID

from psycopg2.extensions import connection
from pymongo import MongoClient
from redis import Redis

from core.logger import logger
from db.mongo import get_mongo, start
from db.postgres import get_auth_postgres, get_movies_postgres
from db.redis import get_redis
from services import extract, load
from services.state import State


def postgres_to_mongo(
        postgres_auth: connection,
        postgres_movies: connection,
        redis: Redis,
        mongo: MongoClient,
):
    state = State(redis)
    while True:
        try:
            users_extractor = extract.PostgresExtractor(postgres_auth, 'users')
            users_timestamp = state.get('users_last_updated', datetime.min)
            for user_id in users_extractor.get_updates(users_timestamp):
                load.create_user_by_id(mongo, UUID(user_id))
        except extract.UpdatesNotFoundError:
            logger.info('Нет обновлений в postgres users')
        else:
            logger.info('Есть обновления в postgres users')
            state.set(
                'users_last_updated',
                datetime.now(tz=timezone(timedelta(hours=3))).strftime('%Y-%m-%dT%H:%M:%S'),
            )

        try:
            movies_extractor = extract.PostgresExtractor(postgres_movies, 'film_work')
            movies_timestamp = state.get('filmworks_last_updated', datetime.min)
            for filmwork_id in movies_extractor.get_updates(movies_timestamp):
                load.create_filmwork_by_id(mongo, UUID(filmwork_id))
        except extract.UpdatesNotFoundError:
            logger.info('Нет обновлений в postgres filmworks')
        else:
            logger.info('Есть обновления в postgres filmworks')
            state.set(
                'filmworks_last_updated',
                datetime.now(tz=timezone(timedelta(hours=3))).strftime('%Y-%m-%dT%H:%M:%S'),
            )

        time.sleep(60)


def main():
    with get_auth_postgres() as postgres_auth_connection:
        with get_movies_postgres() as postgres_movies_connection:
            with get_redis() as redis_connection:
                with get_mongo() as mongo_connection:
                    postgres_to_mongo(
                        postgres_auth_connection,
                        postgres_movies_connection,
                        redis_connection,
                        mongo_connection,
                    )


if __name__ == '__main__':
    start()
    main()
