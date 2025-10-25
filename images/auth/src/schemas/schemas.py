from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    status: str


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


class SignUpSchema(BaseModel):
    email: str
    password: str


class SignInSchema(SignUpSchema):
    pass


class ConfirmCodeSchema(BaseModel):
    code: str


class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str


class EmailSchema(BaseModel):
    email: str


class UserSessionSchema(BaseModel):
    user_id: str
    user_agent: str
    event_date: datetime
    user_device_type: str
