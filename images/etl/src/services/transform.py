from dataclasses import dataclass
from typing import Iterator

from psycopg2.extras import DictRow
from redis import Redis

from models.filmwork import Filmwork
from models.person import Person


@dataclass
class DataTransform(object):
    """Класс для преобразования данных и хранения в Redis промежуточных результатов."""

    redis: Redis

    def add_film_work_ids(self, film_work_ids: list[str]) -> None:
        """Добавляют данные в список первичный ключей кинопроизведений."""
        if film_work_ids != [] and film_work_ids is not None:
            self.redis.lpush('film_work_ids', *film_work_ids)

    def get_film_work_ids(self) -> list[str]:
        """Возвращает и очищает список первичный ключей кинопроизведений из Redis."""
        data = self.redis.lrange('film_work_ids', 0, -1)
        self.redis.delete('film_work_ids')
        return data

    def transform_film_works(self, film_works: Iterator[DictRow]) -> list[Filmwork]:
        pydantic_film_works = []
        film_works = [dict(film_work) for film_work in film_works]
        for film_work in film_works:
            if film_work['person_ids']:
                film_work['person_roles'] = [
                    person_role.strip() for person_role in film_work['person_roles'].split(',')
                ]
                film_work['person_ids'] = [
                    person_id.strip() for person_id in film_work['person_ids'].split(',')
                ]
                film_work['person_names'] = [
                    person_name.strip() for person_name in film_work['person_names'].split(',')
                ]
            film_work['genre_names'] = [
                genre_name.strip() for genre_name in film_work['genre_names'].split(',')
            ]
            directors: list[Person] = []
            actors: list[Person] = []
            writers: list[Person] = []
            if film_work['person_ids']:
                for i in range(len(film_work['person_ids'])):
                    person = Person(
                        id=film_work['person_ids'][i],
                        full_name=film_work['person_names'][i],
                    )
                    if film_work['person_roles'][i] == 'director':
                        directors.append(person)
                    if film_work['person_roles'][i] == 'actor':
                        actors.append(person)
                    if film_work['person_roles'][i] == 'writer':
                        writers.append(person)
            pydantic_film_works.append(
                Filmwork(
                    id=film_work['id'],
                    title=film_work['title'],
                    description=film_work['description'],
                    rating=film_work['rating'] if film_work['rating'] else 0.0,
                    genres=film_work['genre_names'],
                    directors=directors,
                    actors=actors,
                    writers=writers,
                    directors_names=[director.name for director in directors],
                    actors_names=[actor.name for actor in actors],
                    writers_names=[writer.name for writer in writers],
                ),
            )
        return pydantic_film_works