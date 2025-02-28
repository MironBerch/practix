from typing import ClassVar

from models.base import UUIDMixin


class BasePerson(UUIDMixin):
    """Базовая модель персоны."""

    _index: ClassVar[str] = 'persons'


class Person(BasePerson):
    """Модель персоны."""

    full_name: str


class FilmworkPerson(BasePerson):
    """Модель персоны для киноработ."""

    name: str
