from typing import Any
from uuid import UUID

from marshmallow import Schema, fields, post_load
from pydantic import BaseModel, Field

from models.session import Session


class Notification(BaseModel):
    user_id: UUID | None = None
    user_email: str | None = None
    subject: str
    template_id: UUID | None = None
    context: dict[str, Any] | None = None
    text: str | None = None
    priority: int = Field(default=5, gt=-1, le=255)

    class Config:
        populate_by_name = True


class SignUpSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, min_length=6)


class SignInSchema(SignUpSchema):
    ...


class ConfirmCodeSchema(Schema):
    code = fields.String(required=True, min_length=6, max_length=6)


class PasswordChangeSchema(Schema):
    old_password = fields.String(required=True, min_length=6)
    new_password = fields.String(required=True, min_length=6)


class EmailSchema(Schema):
    email = fields.Email(required=True)


class UserSessionSchema(Schema):
    user_id = fields.String(load_only=True)
    user_agent = fields.String()
    event_date = fields.DateTime(dump_only=True)
    user_device_type = fields.String()

    @post_load
    def create_user_history(self, data, **kwargs):
        session = Session(**data)
        return session
