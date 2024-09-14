import uuid
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db


class Session(db.Model):
    """Модель сессии пользователя."""

    __tablename__ = 'sessions'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    event_date = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    user_agent = db.Column(db.String)
    user_device_type = db.Column(db.String, primary_key=True)
