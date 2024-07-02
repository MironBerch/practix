from typing import ClassVar

from pydantic import Field

from models.base import UUIDMixin


class Person(UUIDMixin):
    """Модель персоны."""

    name: str = Field(alias='full_name')
    _index: ClassVar[str] = 'persons'
