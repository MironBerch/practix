from dataclasses import dataclass
from datetime import date, datetime
from typing import Type, Union
from uuid import UUID


@dataclass
class TimeStampedMixin:
    created_at: datetime
    updated_at: datetime


@dataclass
class UUIDMixin:
    id: UUID


@dataclass
class Genre(UUIDMixin, TimeStampedMixin):
    name: str
    description: str | None

    def to_tuple(self) -> tuple[UUID | str | datetime | None, ...]:
        return (
            self.id,
            self.name,
            self.description or '',
            self.created_at,
            self.updated_at,
        )

    @classmethod
    def db_table_name(cls) -> str:
        return 'content.genre'

    @classmethod
    def get_db_field_names(cls) -> tuple[str, ...]:
        return ('id', 'name', 'description', 'created_at', 'updated_at')


@dataclass
class Person(UUIDMixin, TimeStampedMixin):
    full_name: str

    def to_tuple(self) -> tuple[UUID | str | datetime, ...]:
        return (self.id, self.full_name, self.created_at, self.updated_at)

    @classmethod
    def db_table_name(cls) -> str:
        return 'content.person'

    @classmethod
    def get_db_field_names(cls) -> tuple[str, ...]:
        return ('id', 'full_name', 'created_at', 'updated_at')


@dataclass
class Filmwork(UUIDMixin, TimeStampedMixin):
    title: str
    description: str | None
    release_date: date | None
    rating: float | None
    access_type: str
    type: str
    age_rating: str

    def to_tuple(self) -> tuple[UUID | str | date | float | datetime | None, ...]:
        return (
            self.id,
            self.title,
            self.description or '',
            self.release_date,
            self.rating,
            self.access_type,
            self.type,
            self.age_rating,
            self.created_at,
            self.updated_at,
        )

    @classmethod
    def db_table_name(cls) -> str:
        return 'content.film_work'

    @classmethod
    def get_db_field_names(cls) -> tuple[str, ...]:
        return (
            'id',
            'title',
            'description',
            'release_date',
            'rating',
            'access_type',
            'type',
            'age_rating',
            'created_at',
            'updated_at',
        )


@dataclass
class GenreFilmwork(UUIDMixin):
    film_work_id: UUID
    genre_id: UUID
    created_at: datetime

    def to_tuple(self) -> tuple[UUID | datetime, ...]:
        return (
            self.id,
            self.film_work_id,
            self.genre_id,
            self.created_at,
        )

    @classmethod
    def db_table_name(cls) -> str:
        return 'content.genre_film_work'

    @classmethod
    def get_db_field_names(cls) -> tuple[str, ...]:
        return ('id', 'film_work_id', 'genre_id', 'created_at')


@dataclass
class PersonFilmwork(UUIDMixin):
    film_work_id: UUID
    person_id: UUID
    role: str
    created_at: datetime

    def to_tuple(self) -> tuple[UUID | str | datetime, ...]:
        return (
            self.id,
            self.film_work_id,
            self.person_id,
            self.role,
            self.created_at,
        )

    @classmethod
    def db_table_name(cls) -> str:
        return 'content.person_film_work'

    @classmethod
    def get_db_field_names(cls) -> tuple[str, ...]:
        return ('id', 'film_work_id', 'person_id', 'role', 'created_at')


Schema = Union[
    Type[Filmwork],
    Type[Genre],
    Type[Person],
    Type[GenreFilmwork],
    Type[PersonFilmwork],
]

schemas: dict[str, Schema] = {
    'film_works': Filmwork,
    'genres': Genre,
    'persons': Person,
    'genre_film_work': GenreFilmwork,
    'person_film_works': PersonFilmwork,
}
