from uuid import UUID

from pydantic import BaseModel


class FilmworkBookmark(BaseModel):
    """Модель ответа для представления закладки."""

    filmwork_id: UUID
