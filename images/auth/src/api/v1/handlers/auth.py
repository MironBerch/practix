from http import HTTPStatus
from typing import Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import redis
from src.db.postgres import get_async_session
from src.dependencies.auth_deps import (
    get_current_user_refresh,
    get_current_user_temp,
    security,
)
from src.models.user import User
from src.schemas.schemas import ConfirmCodeSchema, Notification, SignInSchema, SignUpSchema
from src.utils import code, hash_password, notification, sessions
from src.utils.jwt_manager import jwt_manager

router = APIRouter(tags=['auth'])


def create_full_tokens(user_id: str) -> tuple[str, str]:
    """Создание access и refresh токенов"""
    access_token = jwt_manager.create_access_token(user_id)
    refresh_token = jwt_manager.create_refresh_token(user_id)
    return access_token, refresh_token


@router.post('/signup', status_code=HTTPStatus.CREATED)
async def signup(
    data: SignUpSchema,
    db: AsyncSession = Depends(get_async_session),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """User sign up"""
    try:
        result = await db.execute(select(User).where(User.email == data.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='User with this email exists'
            )

        user = User(
            email=data.email,
            password_hash=hash_password.hash_password(data.password),
            is_active=True,
            is_email_confirmed=False,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        verification_code = await code.create_registration_email_verification_code(
            user.email, cache_adapter
        )
        await notification.send_notification(
            data=Notification(
                user_email=user.email,
                subject=f'{verification_code} — ваш код для подтверждения регистрации',
                text=f'Код {verification_code}. Код действителен в течение 10 минут',
            ).model_dump(),
        )
        temp_token = jwt_manager.create_temp_token(str(user.id))
        return {
            'message': 'user created',
            'temp_token': temp_token,
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/resend_confirm_registration_email', status_code=HTTPStatus.OK)
async def resend_confirm_registration_email(
    user_id: str = Depends(get_current_user_temp),
    db: AsyncSession = Depends(get_async_session),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """Resend confirmation registration email"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    verification_code = await code.create_registration_email_verification_code(
        user.email, cache_adapter
    )
    await notification.send_notification(
        data=Notification(
            user_email=user.email,
            subject=f'{verification_code} — ваш код для подтверждения регистрации',
            text=f'Код {verification_code}. Код действителен в течение 10 минут',
        ).model_dump(),
    )
    return {'message': 'code sent to email'}


@router.post('/confirm_registration', status_code=HTTPStatus.OK)
async def confirm_registration(
    data: ConfirmCodeSchema,
    request: Request,
    user_id: str = Depends(get_current_user_temp),
    db: AsyncSession = Depends(get_async_session),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """Confirm registration with verification code"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    code_from_cache = await cache_adapter.get_object_from_cache(f'email_registration:{user.email}')
    if code_from_cache is not None and code_from_cache == data.code:
        user.is_email_confirmed = True
        await db.commit()
        access_token, refresh_token = create_full_tokens(str(user.id))
        await sessions.create_session(
            user_id=user.id,
            user_agent=request.headers.get('User-Agent'),
            db=db,
        )
        return {
            'message': 'email confirmed',
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='code is not correct')


@router.post('/signin', status_code=HTTPStatus.OK)
async def signin(
    data: SignInSchema,
    db: AsyncSession = Depends(get_async_session),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """User sign in"""
    try:
        stmt = select(User).where(User.email == data.email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='user with this email does not exist'
            )

        if not hash_password.check_password(user.password_hash, data.password):
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='password is not correct')

        temp_token = jwt_manager.create_temp_token(str(user.id))
        verification_code = await code.create_2_step_verification_code(user.email, cache_adapter)
        await notification.send_notification(
            data=Notification(
                user_email=user.email,
                subject=f'{verification_code} — ваш код для входа',
                text=f'Код {verification_code}. Код действителен в течение 10 минут',
            ).model_dump(),
        )
        return {
            'temp_token': temp_token,
            'message': '2-step verification code sent to email.',
        }
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/resend_2_step_verification_email', status_code=HTTPStatus.OK)
async def resend_2_step_verification_email(
    user_id: str = Depends(get_current_user_temp),
    db: AsyncSession = Depends(get_async_session),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """Resend two-step verification email"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    verification_code = await code.create_2_step_verification_code(user.email, cache_adapter)
    await notification.send_notification(
        data=Notification(
            user_email=user.email,
            subject=f'{verification_code} — ваш код для входа',
            text=f'Код {verification_code}. Код действителен в течение 10 минут',
        ).model_dump(),
    )
    return {'message': 'new verification code sent to email'}


@router.post('/confirm_2_step_verification', status_code=HTTPStatus.OK)
async def confirm_2_step_verification(
    data: ConfirmCodeSchema,
    request: Request,
    user_id: str = Depends(get_current_user_temp),
    db: AsyncSession = Depends(get_async_session),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """Confirm two-step verification with verification code"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    code_from_redis = await cache_adapter.get_object_from_cache(
        f'2_step_verification_code:{user.email}'
    )
    if code_from_redis is not None and code_from_redis == data.code:
        access_token, refresh_token = create_full_tokens(str(user.id))
        await sessions.create_session(
            user_id=user.id,
            user_agent=request.headers.get('User-Agent'),
            db=db,
        )
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail='code is not correct or has expired'
    )


@router.post('/logout', status_code=HTTPStatus.OK)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
) -> dict[str, Any]:
    """User log out"""
    token = credentials.credentials
    try:
        # Получаем payload без проверки expiration (чтобы можно было logout с просроченным токеном)
        payload = jwt_manager.get_token_payload(token)
        jti = payload.get('jti')
        exp_timestamp = payload.get('exp')

        if jti and exp_timestamp:
            # Вычисляем TTL для blacklist
            exp_datetime = datetime.fromtimestamp(exp_timestamp)
            now = datetime.now(timezone.utc)
            ttl = max(0, int((exp_datetime - now).total_seconds()))

            if ttl > 0:
                await cache_adapter.put_object_to_cache(f'blacklist:{jti}', 'revoked', ex=ttl)

        return {'message': 'logout completed'}
    except HTTPException:
        # Если токен невалидный, все равно считаем logout успешным
        return {'message': 'logout completed'}


@router.post('/refresh', status_code=HTTPStatus.OK)
async def refresh(
    user_id: str = Depends(get_current_user_refresh),
    cache_adapter: redis.RedisAdapter = Depends(redis.get_redis_adapter),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    """Refresh token"""
    # Добавляем старый refresh токен в blacklist
    old_token = credentials.credentials
    old_payload = jwt_manager.get_token_payload(old_token)
    old_jti = old_payload.get('jti')
    old_exp = old_payload.get('exp')

    if old_jti and old_exp:
        from datetime import datetime

        exp_datetime = datetime.fromtimestamp(old_exp)
        now = datetime.now(timezone.utc)
        ttl = max(0, int((exp_datetime - now).total_seconds()))

        if ttl > 0:
            await cache_adapter.put_object_to_cache(f'blacklist:{old_jti}', 'refreshed', ex=ttl)

    # Создаем новый access токен
    access_token = jwt_manager.create_access_token(user_id)

    return {'access_token': access_token}
