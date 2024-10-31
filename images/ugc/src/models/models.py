from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FilmworkBookmark(BaseModel):
    """Модель ответа для представления закладки."""

    filmwork_id: UUID


class Text(BaseModel):
    text: str


class Review(BaseModel):
    """Модель ответа для представления рецензии на фильм."""

    id: UUID
    author_id: UUID
    filmwork_id: UUID
    text: str
    pub_date: datetime
    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
