from models.base import UUIDMixin
from models.person import BasePerson
from datetime import date


class BaseFilmwork(UUIDMixin):
    """Базовая модель фильма."""

    title: str
    rating: float


class Filmwork(BaseFilmwork):
    """Модель фильма."""

    description: str
    release_date: date
    type: str
    genres: list[str]
    actors: list[BasePerson]
    writers: list[BasePerson]
    directors: list[BasePerson]
