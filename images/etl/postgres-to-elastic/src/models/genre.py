from typing import ClassVar

from models.base import UUIDMixin


class BaseGenre(UUIDMixin):
    """Базовая модель жанра фильма."""

    name: str


class Genre(BaseGenre):
    """Модель жанра фильма."""

    description: str
    _index: ClassVar[str] = 'genres'
