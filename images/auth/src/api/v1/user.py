from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from flask import Blueprint, Response, jsonify, request

from src.api.schemas import (
    ConfirmCodeSchema,
    EmailSchema,
    Notification,
    PasswordChangeSchema,
    UserSessionSchema,
)
from src.db import postgres, redis
from src.models.session import Session
from src.models.user import User
from src.utils import code, hash_password, notification

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/user_info', methods=['GET'])
@jwt_required()
def get_user_info() -> tuple[Response, HTTPStatus]:
    """
    Get user info
    ---
    get:
      summary: Get user info
      security:
        - Bearer: []
    responses:
      '200':
        description: Return user info
        schema:
          type: object
          properties:
            user_id:
              type: string
              format: uuid
            user_email:
              type: string
            created_at:
              type: string
              format: date
      '403':
        description: Forbidden error
    tags:
      - user
    """
    identity = get_jwt_identity()
    user: User = User.query.get(identity)
    return (
        jsonify({'user_id': user.id, 'user_created_at': user.created_at, 'user_email': user.email}),
        HTTPStatus.OK,
    )


@bp.route('/password_change', methods=['POST'])
@jwt_required()
def password_change() -> tuple[Response, HTTPStatus]:
    """
    Change user password
    ---
    post:
      summary: Password change
      parameters:
      - name: user
        in: body
        description: Old and new passwords
        required: true
        schema:
          type: object
          properties:
            old_password:
              type: string
              description: old password
            old_password:
              type: string
              description: new password
    responses:
      '201':
        description: Password changed correctly
    tags:
      - user
    """
    try:
        identity = get_jwt_identity()
        data = PasswordChangeSchema().load(request.get_json())
        user = User.query.get(identity)
        if not hash_password.check_password(user.password_hash, data['old_password']):
            raise ValidationError('old password is not correct')
        user.password_hash = hash_password.hash_password(data['new_password'])
        postgres.db.session.commit()
        return jsonify({'message': 'password changed'}), HTTPStatus.CREATED
    except ValidationError as err:
        return jsonify({'message': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/change_email', methods=['POST'])
@jwt_required()
def change_email() -> tuple[Response, HTTPStatus]:
    """
    Change user email
    ---
    post:
      summary: Change user email
      parameters:
      - name: user
        in: body
        description: user email
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: email
    responses:
      '201':
        description: Change email sended
    tags:
      - user
    """
    try:
        identity = get_jwt_identity()
        data = EmailSchema().load(request.get_json())
        user = User.query.get(identity)
        if User.query.filter_by(email=data['email']).first():
            raise ValidationError('user with this email exist')
        verification_code = code.create_change_email_verification_code(user.email, data['email'])
        notification.send_notification(
            data=Notification(
                user_email=data['email'],
                subject=f'{verification_code} — ваш код для подтверждения электронной почты',
                text=f'Код {verification_code}. Код действителен в течение 10 минут',
            ).model_dump(),
        )
        return jsonify({'message': 'email changed'}), HTTPStatus.CREATED
    except ValidationError as err:
        return jsonify({'message': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/resend_change_email', methods=['POST'])
@jwt_required()
def resend_change_email() -> tuple[Response, HTTPStatus]:
    """
    Resend change email
    ---
    post:
      summary: Resend change email
      security:
        - Bearer: []
    responses:
      '200':
        description: Code sent successfully to the email
        schema:
          type: object
          properties:
            message:
              type: string
              description: Confirmation message
      '401':
        description: Unauthorized
    tags:
      - user
    """
    identity = get_jwt_identity()
    user = User.query.get(identity)
    verification_code = redis.redis.get(f'email_change:{user.email}')
    if verification_code is None:
        return jsonify({'message': 'no code for your email'}), HTTPStatus.BAD_REQUEST
    old_verification_code = verification_code.split(':')
    verification_code = code.create_change_email_verification_code(
        old_email=user.email,
        new_email=old_verification_code[0],
    )
    notification.send_notification(
        data=Notification(
            user_email=old_verification_code[0],
            subject=f'{verification_code} — ваш код для подтверждения электронной почты',
            text=f'Код {verification_code}. Код действителен в течение 10 минут',
        ).model_dump(),
    )
    return jsonify({'message': 'code sended on email'}), HTTPStatus.OK


@bp.route('/confirm_change_email', methods=['POST'])
@jwt_required()
def confirm_change_email() -> tuple[Response, HTTPStatus]:
    """
    Confirm email for change with verification code
    ---
    post:
      summary: Confirm change email
      security:
        - Bearer: []
      parameters:
      - name: code
        in: body
        required: true
        schema:
          type: object
          properties:
            code:
              type: string
              description: Verification code sent to email
    responses:
      '200':
        description: Email confirmed successfully
        schema:
          type: object
          properties:
            message:
              type: string
              description: Confirmation message
      '400':
        description: Invalid code
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message
    tags:
      - user
    """
    data = ConfirmCodeSchema().load(request.get_json())
    identity = get_jwt_identity()
    user = User.query.get(identity)
    verification_code = redis.redis.get(f'email_change:{user.email}')
    if verification_code is not None:
        verification_code = verification_code.split(':')
        if verification_code[-1] == data['code']:
            user.email = verification_code[0]
            user.is_email_confirmed = True
            postgres.db.session.commit()
            return jsonify({'message': 'email confirmed'}), HTTPStatus.OK
    return jsonify({'message': 'code is not correct'}), HTTPStatus.BAD_REQUEST


@bp.route('/user_sessions', methods=['GET'])
@jwt_required()
def get_user_sessions() -> tuple[Response, HTTPStatus]:
    """
    Get user sessions
    ---
    get:
      summary: Get user sessions
      security:
        - Bearer: []
    responses:
      '200':
        description: Return sessions
        schema:
          type: object
          properties:
            user_id:
              type: string
              format: uuid
            user_agent:
              type: string
            user_device_type:
              type: string
            date:
              type: string
              format: date
      '403':
        description: Forbidden error
    tags:
      - user
    """
    identity = get_jwt_identity()
    user = User.query.get(identity)
    paginated_user_sessions = Session.query.filter_by(user_id=user.id).paginate(
        page=request.args.get('page', default=1, type=int),
        per_page=request.args.get('count', default=10, type=int),
    )
    return (
        jsonify(
            UserSessionSchema().dump(
                paginated_user_sessions.items,
                many=True,
            ),
        ),
        HTTPStatus.OK,
    )
