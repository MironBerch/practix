from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class CustomBaseModel(BaseModel):
    class Config:
        populate_by_name = True


class UUIDMixin(CustomBaseModel):
    id: UUID = Field(alias='uuid')


class User(UUIDMixin):
    email: str


class Notification(CustomBaseModel):
    user_id: UUID
    subject: str
    template_id: UUID | None = None
    context: dict[str, Any] | None = None
    text: str | None = None
    priority: int = Field(default=5, gt=-1, le=255)

    @model_validator(mode='before')
    def check_notification_fields(cls, values: dict):
        error_message = 'Must specify at least "text" or "template_id" and "context"'

        text = values.get('text')
        template_id = values.get('template_id')
        context = values.get('context')

        if text is not None or (template_id is not None and context is not None):
            return values

        raise ValueError(error_message)
