from typing import ClassVar

from pydantic import RootModel

from models.base import UUIDMixin


class Genre(UUIDMixin):
    """Модель жанра."""

    name: str
    description: str


class GenreList(RootModel):
    """Список жанров."""

    root: list[Genre]
    item: ClassVar[type] = Genre
