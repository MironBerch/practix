from typing import ClassVar

from pydantic import validator

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

    @validator('actors', 'writers', 'directors', each_item=True)
    @classmethod
    def change_person_field(cls, person: Person) -> dict:
        """Валидатор для смены названия поля полного имени персоны."""
        return {'id': person.id, 'name': person.name}
