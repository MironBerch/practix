from typing import ClassVar

from models.base import UUIDMixin
from models.person import Person


class Filmwork(UUIDMixin):
    """Модель кинопроизведения."""

    title: str
    description: str
    genres: list[str]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    _index: ClassVar[str] = 'movies'
