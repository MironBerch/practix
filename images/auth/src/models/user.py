import uuid

from db.postgres import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        uuid.UUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    email = db.Column(
        db.String(255),
        unique=True,
        index=True,
    )
    password_hash = db.Column(db.String(255))
