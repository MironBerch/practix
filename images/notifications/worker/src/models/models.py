from typing import Any
from uuid import UUID

from pydantic import BaseModel


class Notification(BaseModel):
    user_id: UUID
    subject: str
    template_id: UUID | None = None
    context: dict[str, Any] | None = None
    text: str | None = None
    priority: int

    class Config:
        populate_by_name = True
