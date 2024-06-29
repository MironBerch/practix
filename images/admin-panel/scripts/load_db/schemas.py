from dataclasses import dataclass
from datetime import date, datetime
from typing import Union
from uuid import UUID


@dataclass
class TimeStampedMixin:
    created_at: datetime
    updated_at: datetime


@dataclass
class UUIDMixin:
    id: UUID


@dataclass
class GenreSQLite(UUIDMixin, TimeStampedMixin):
    name: str
    description: str | None

    def to_tuple(self) -> tuple:
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
    def get_db_field_names(cls) -> tuple[str]:
        return ('id', 'name', 'description', 'created_at', 'updated_at')


@dataclass
class PersonSQLite(UUIDMixin, TimeStampedMixin):
    full_name: str

    def to_tuple(self) -> tuple:
        return (self.id, self.full_name, self.created_at, self.updated_at)

    @classmethod
    def db_table_name(cls) -> str:
        return 'content.person'

    @classmethod
    def get_db_field_names(cls) -> tuple[str]:
        return ('id', 'full_name', 'created_at', 'updated_at')


@dataclass
class FilmworkSQLite(UUIDMixin, TimeStampedMixin):
    title: str
    description: str | None
    release_date: date | None
    rating: float | None
    access_type: str
    type: str
    age_rating: str

    def to_tuple(self) -> tuple:
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
    def get_db_field_names(cls) -> tuple[str]:
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
class GenreFilmworkSQLite(UUIDMixin):
    film_work_id: UUID
    genre_id: UUID
    created_at: datetime

    def to_tuple(self) -> tuple:
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
    def get_db_field_names(cls) -> tuple[str]:
        return ('id', 'film_work_id', 'genre_id', 'created_at')


@dataclass
class PersonFilmworkSQLite(UUIDMixin):
    film_work_id: UUID
    person_id: UUID
    role: str
    created_at: datetime

    def to_tuple(self) -> tuple:
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
    def get_db_field_names(cls) -> tuple[str]:
        return ('id', 'film_work_id', 'person_id', 'role', 'created_at')


SQLiteSchema = Union[
    FilmworkSQLite,
    GenreSQLite,
    PersonSQLite,
    GenreFilmworkSQLite,
    PersonFilmworkSQLite,
]

schemas: dict[str, SQLiteSchema] = {
    'film_works': FilmworkSQLite,
    'genres': GenreSQLite,
    'persons': PersonSQLite,
    'genre_film_work': GenreFilmworkSQLite,
    'person_film_works': PersonFilmworkSQLite,
}
