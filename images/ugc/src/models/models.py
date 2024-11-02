from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class FilmworkBookmark(BaseModel):
    """Модель ответа для представления закладки."""

    filmwork_id: UUID


class Text(BaseModel):
    text: str


class Score(BaseModel):
    score: int


class Review(BaseModel):
    """Модель ответа для представления рецензии на фильм."""

    id: UUID
    author_id: UUID
    filmwork_id: UUID
    text: str
    pub_date: datetime


class Vote(BaseModel):
    user_id: UUID
    score: float = Field(gt=0, le=10)


class Rating(BaseModel):
    average_rating: int | None
    votes: list[Vote] | None = Field(exclude=True)

    @model_validator(mode='before')
    @classmethod
    def scoring(cls, data: dict) -> dict:
        """
        Валидатор для подсчета средней пользовательской оценки.
        """
        votes: list[Vote] = data.get('votes')
        if votes:
            data['average_rating'] = sum([vote.score for vote in votes]) // (len(votes))
        return data
