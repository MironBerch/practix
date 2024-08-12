import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db


class User(db.Model):
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
