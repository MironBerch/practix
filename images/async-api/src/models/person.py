from typing import ClassVar
from uuid import UUID

from pydantic import Field, RootModel

from models.base import UUIDMixin


class BasePerson(UUIDMixin):
    """Базовая модель персоны."""

    full_name: str = Field(alias='name')


class Person(UUIDMixin):
    """Модель персоны."""

    roles: list[str]
    filmwork_ids: list[UUID]


class PersonList(RootModel):
    """Список персон."""

    root: list[Person]
    item: ClassVar[type] = Person
