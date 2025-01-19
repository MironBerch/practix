from aio_pika import Connection, DeliveryMode, Message
from db.postgres import User, get_db
from db.rabbitmq import get_rabbitmq
from models.models import Notification
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


@router.post(
    '/notification',
    response_model=Notification,
    summary='Publish notification',
    description='Publish notification for user',
)
async def publish_notification(
    notification: Notification,
    rabbitmq: Connection = Depends(get_rabbitmq),
) -> Notification:
    async with rabbitmq.channel() as channel:
        await channel.declare_queue(
            'notification_queue',
            durable=True,
        )
        message_body = notification.model_dump_json()
        message = Message(
            body=message_body.encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            priority=notification.priority,
        )
        await channel.default_exchange.publish(
            message,
            routing_key='notification_queue',
        )
    return notification
