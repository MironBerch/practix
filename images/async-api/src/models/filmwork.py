from typing import ClassVar, Type

from pydantic import RootModel

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


class FilmworkList(RootModel):
    """Список фильмов с краткой информацией."""

    root: list[BaseFilmwork]
    item: ClassVar[Type] = BaseFilmwork
