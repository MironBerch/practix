import uuid
from datetime import datetime, timezone

from sqlalchemy import Table, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import Connection
from sqlalchemy.orm import validates
from user_agents import parse as parse_user_agent
from werkzeug.user_agent import UserAgent

from src.db.postgres import db


def create_partition(target: Table, connection: Connection, **kwargs) -> None:
    """
    Функция для партицирования таблицы `sessions` по типам устройств.
    """

    device_types = ('pc', 'tablet', 'mobile', 'other')
    for device_type in device_types:
        connection.execute(
            statement=text(
                text=f"""
                    CREATE TABLE IF NOT EXISTS "sessions_{device_type}"
                    PARTITION OF "sessions" FOR VALUES IN ('{device_type}')
                """
            )
        )


class Session(db.Model):
    """Модель сессии пользователя."""

    __tablename__ = 'sessions'
    __table_args__ = {
        'postgresql_partition_by': 'LIST (user_device_type);',
        'listeners': [('after_create', create_partition)],
    }

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

    @validates('user_device_type')
    def validate_user_device_type(self, key: str, value: UserAgent) -> str:
        """
        Парсит данные `User-agent` и определяет с какого устройства вошёл пользователь.
        """

        device = None
        user_agent = parse_user_agent(value)
        if user_agent.is_pc:
            device = 'pc'
        elif user_agent.is_tablet:
            device = 'tablet'
        elif user_agent.is_mobile:
            device = 'mobile'
        return device or 'other'
