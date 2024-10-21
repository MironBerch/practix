from typing import ClassVar

from pydantic import field_validator

from models.base import UUIDMixin
from models.person import Person


class Filmwork(UUIDMixin):
    """Модель кинопроизведения."""

    title: str
    description: str
    rating: float = 0.0
    genres: list[str]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    _index: ClassVar[str] = 'movies'

    @field_validator('actors', 'writers', 'directors', mode='before')
    @classmethod
    def change_persons_field(cls, persons: list[Person]) -> list[dict]:
        """Валидатор для смены названия поля полного имени персоны."""
        return [{'id': person.id, 'name': person.name} for person in persons]
