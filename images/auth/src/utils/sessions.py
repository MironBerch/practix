from uuid import UUID

from db.postgres import db
from models.session import Session


def create_session(
        user_id: str | UUID,
        user_agent: str,
):
    new_session = Session(
        user_id=user_id,
        user_agent=user_agent,
    )
    try:
        db.session.add(new_session)
        db.session.commit()
    except Exception:
        db.session.rollback()