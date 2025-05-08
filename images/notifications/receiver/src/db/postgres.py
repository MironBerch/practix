import uuid

from sqlalchemy import Column, DateTime, String, Text, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from core.config import settings

DATABASE_URL = (
    f'postgresql://{settings.postgres.user}:{settings.postgres.password}'
    f'@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}'
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)


class Template(Base):
    __tablename__ = 'templates'

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    code = Column(Text, nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
