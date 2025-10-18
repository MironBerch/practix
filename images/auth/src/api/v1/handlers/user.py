from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import redis
from src.db.postgres import get_async_session
from src.dependencies.auth_deps import get_current_user
from src.models.session import Session
from src.models.user import User
from src.schemas.schemas import (
    ConfirmCodeSchema,
    EmailSchema,
    Notification,
    PasswordChangeSchema,
    UserSessionSchema,
)
from src.utils import code, hash_password, notification

router = APIRouter(tags=['user'])


@router.get('/user_info', status_code=HTTPStatus.OK)
async def get_user_info(
    user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)
) -> dict[str, Any]:
    """Get user info"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return {
        'user_id': user.id,
        'user_created_at': user.created_at,
        'user_email': user.email,
        'is_email_confirmed': user.is_email_confirmed,
    }


@router.post('/password_change', status_code=HTTPStatus.OK)
async def password_change(
    data: PasswordChangeSchema,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, Any]:
    """Change user password"""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

        user.password_hash = hash_password.hash_password(data.new_password)
        await db.commit()
        return {'message': 'password changed'}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/change_email', status_code=HTTPStatus.OK)
async def change_email(
    data: EmailSchema,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """Change user email"""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

        stmt = select(User).where(User.email == data.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='user with this email exist'
            )

        verification_code = await code.create_change_email_verification_code(
            user.email, data.email, cache_adapter
        )
        await notification.send_notification(
            data=Notification(
                user_email=data.email,
                subject=f'{verification_code} — ваш код для подтверждения электронной почты',
                text=f'Код {verification_code}. Код действителен в течение 10 минут',
            ).model_dump(),
        )
        return {'message': 'email changed'}

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/resend_change_email', status_code=HTTPStatus.OK)
async def resend_change_email(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """Resend change email"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    verification_code = await cache_adapter.get_object_from_cache(f'email_change:{user.email}')
    if verification_code is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='no code for your email')

    old_verification_code = verification_code.split(':')
    verification_code = await code.create_change_email_verification_code(
        old_email=user.email,
        new_email=old_verification_code[0],
        redis_adapter=cache_adapter,
    )
    await notification.send_notification(
        data=Notification(
            user_email=old_verification_code[0],
            subject=f'{verification_code} — ваш код для подтверждения электронной почты',
            text=f'Код {verification_code}. Код действителен в течение 10 минут',
        ).model_dump(),
    )
    return {'message': 'code sent to email'}


@router.post('/confirm_change_email', status_code=HTTPStatus.OK)
async def confirm_change_email(
    data: ConfirmCodeSchema,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """Confirm email for change with verification code"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    verification_code = await cache_adapter.get_object_from_cache(f'email_change:{user.email}')
    if verification_code is not None:
        verification_code_parts = verification_code.split(':')
        if verification_code_parts[-1] == data.code:
            user.email = verification_code_parts[0]
            user.is_email_confirmed = True
            await db.commit()
            return {'message': 'email confirmed'}

    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='code is not correct')


@router.get('/user_sessions', status_code=HTTPStatus.OK)
async def get_user_sessions(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> List[UserSessionSchema]:
    """Get user sessions"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    stmt = select(Session).where(Session.user_id == user.id)
    result = await db.execute(stmt)
    user_sessions = result.scalars().all()

    return [
        UserSessionSchema(
            user_id=str(session.user_id),
            user_agent=session.user_agent,
            event_date=session.event_date,
            user_device_type=session.user_device_type,
        )
        for session in user_sessions
    ]
