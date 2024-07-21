from models.base import UUIDMixin
from models.person import BasePerson


class BaseFilmwork(UUIDMixin):
    """Базовая модель фильма."""

    title: str
    rating: float


class Filmwork(BaseFilmwork):
    """Модель фильма."""

    description: str
    genres: list[str]
    actors: list[BasePerson]
    writers: list[BasePerson]
    directors: list[BasePerson]
