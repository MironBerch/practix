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
    template_id: UUID | None = None
    context: dict[str, Any] | None = None
    text: str | None = None
    priority: int = Field(default=5, gt=-1, le=255)

    @model_validator(mode='before')
    def check_notification_fields(cls, values: dict):
        error_message = (
            "Either 'text' must be provided or both 'template_id' and "
            "'context' must be provided, but not both options together."
        )

        text = values.get('text')
        template_id = values.get('template_id')
        context = values.get('context')

        use_template = text is None and (template_id is not None and context is not None)
        not_use_template = text is not None and (template_id is None and context is None)

        if use_template or not_use_template:
            return values

        raise ValueError(error_message)
