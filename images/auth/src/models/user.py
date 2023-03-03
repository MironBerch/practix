import uuid
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db


class User(db.Model):
    """Модель пользователя."""

    __tablename__ = 'users'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email = db.Column(
        db.String(255),
        unique=True,
        index=True,
    )

    password_hash = db.Column(db.String(255))

    is_active = db.Column(db.Boolean())
    is_email_confirmed = db.Column(db.Boolean())

    created_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
    )

    sessions = db.relationship(
        'Session',
        backref=db.backref('user', lazy='joined'),
        lazy='dynamic',
        order_by='Session.event_date.desc()',
        passive_deletes=True,
    )
