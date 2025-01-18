from db.postgres import User, get_db
from models.models import User as UserSchema
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

router = APIRouter(tags=['notifications'])


@router.post(
    '/user',
    response_model=UserSchema,
    summary='Set notifications recipient',
    description='Add new or change existing user to receive notifications',
)
async def set_notifications_recipient(
    user: UserSchema,
    db: Session = Depends(get_db),
) -> User:
    existing_user = db.query(User).filter(User.id == user.id).first()
    if existing_user:
        existing_user.email = user.email
        db.commit()
        db.refresh(existing_user)
        return existing_user
    else:
        new_user = User(id=user.id, email=user.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
