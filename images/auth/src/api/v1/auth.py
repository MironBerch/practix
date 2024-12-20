from datetime import timedelta
from http import HTTPStatus

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError

from flask import Blueprint, current_app, jsonify, request

from api.schemas import ConfirmCodeSchema, SignInSchema, SignUpSchema
from core.config import settings
from db import postgres, redis
from models.user import User
from utils import code, hash_password, sessions, tasks

bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


@bp.route('/signup', methods=['POST'])
def signup():
    """
    User sign up
    ---
    post:
      summary: Register user
      parameters:
      - name: user
        in: body
        description: User registration data
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: email
            password:
              type: string
              description: password
    responses:
      '201':
        description: Created successfully
      '403':
        description: Conflict
    tags:
      - auth
    """
    try:
        data = SignUpSchema().load(request.get_json())
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'User with this email exists'}), HTTPStatus.FORBIDDEN
        user = User(
            email=data['email'],
            password_hash=hash_password.hash_password(data['password']),
            is_active=True,
            is_email_confirmed=False,
        )
        postgres.db.session.add(user)
        postgres.db.session.commit()
        created_user = User.query.filter_by(email=data['email']).first()
        verification_code = code.create_registration_email_verification_code(user.email)
        tasks.send_2_step_verification_code.delay(user.email, verification_code)
        tasks.delete_user_with_not_confirmed_email.apply_async(
          (created_user.id,),
          countdown=60*60,
        )
        temp_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(
                minutes=settings.security.jwt_temp_token_expires,
            ),
        )
        return jsonify(
            {
                'message': 'user created',
                'temp_token': temp_token,
            }
        ), HTTPStatus.CREATED
    except ValidationError as err:
        return jsonify({'message': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/resend_confirm_registration_email', methods=['POST'])
@jwt_required()
def resend_confirm_registration_email():
    """
    Resend confirmation registration email
    ---
    post:
      summary: Resend confirmation email
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
      - auth
    """
    identity = get_jwt_identity()
    user = User.query.get(identity)
    tasks.send_registration_email_verification_code.delay(
        user.email,
        code.create_registration_email_verification_code(user.email),
    )
    return jsonify({'message': 'code sended on email'}), HTTPStatus.OK


@bp.route('/confirm_registration', methods=['POST'])
@jwt_required()
def confirm_registration():
    """
    Confirm registration with verification code
    ---
    post:
      summary: Confirm user registration
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
      - auth
    """
    data = ConfirmCodeSchema().load(request.get_json())
    identity = get_jwt_identity()
    user = User.query.get(identity)
    code = redis.redis.get(f'email_registration:{user.email}')
    if code is not None and code == data['code']:
        user.is_email_confirmed = True
        postgres.db.session.commit()
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        sessions.create_session(
            user_id=user.id,
            user_agent=request.headers.get('User-Agent'),
        )
        return jsonify(
            {
                'message': 'email confirmed',
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        ), HTTPStatus.OK
    return jsonify({'message': 'code is not correct'}), HTTPStatus.BAD_REQUEST


@bp.route('/signin', methods=['POST'])
def signin():
    """
    User sign in
    ---
    post:
      summary: User Sign In
      parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User email
            password:
              type: string
              description: User password
    responses:
      '200':
        description: Successful sign in with temporary token
        schema:
          type: object
          properties:
            temp_token:
              type: string
              description: Temporary JWT token for 2FA
            message:
              type: string
              description: Message confirming code sent for verification
      '403':
        description: Incorrect email or password
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message
      '500':
        description: Server error
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message
    tags:
      - auth
    """
    try:
        data = SignInSchema().load(request.get_json())
        user: User = User.query.filter_by(email=data['email']).first()
        if user is None:
            return jsonify(
                {'message': 'user with this email does not exist'},
            ), HTTPStatus.FORBIDDEN
        if not hash_password.check_password(user.password_hash, data['password']):
            return jsonify({'message': 'password is not correct'}), HTTPStatus.FORBIDDEN
        temp_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(
                minutes=settings.security.jwt_temp_token_expires,
            ),
        )
        tasks.send_2_step_verification_code.delay(
            user.email,
            code.create_2_step_verification_code(user.email),
        )
        return jsonify(
            {
                'temp_token': temp_token,
                'message': '2-step verification code sent to email.',
            },
        ), HTTPStatus.OK
    except ValidationError as err:
        return jsonify({'message': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/resend_2_step_verification_email', methods=['POST'])
@jwt_required()
def resend_2_step_verification_email():
    """
    Resend two-step verification email
    ---
    post:
      summary: Resend two-step verification email
      security:
        - Bearer: []
    responses:
      '200':
        description: New verification code sent successfully
        schema:
          type: object
          properties:
            message:
              type: string
              description: Confirmation message
      '401':
        description: Unauthorized
    tags:
      - auth
    """
    identity = get_jwt_identity()
    user = User.query.get(identity)
    verification_code = code.create_2_step_verification_code(user.email)
    tasks.send_2_step_verification_code.delay(user.email, verification_code)
    return jsonify({'message': 'new verification code sent to email'}), HTTPStatus.OK


@bp.route('/confirm_2_step_verification', methods=['POST'])
@jwt_required()
def confirm_2_step_verification():
    """
    Confirm two-step verification with verification code
    ---
    post:
      summary: Confirm two-step verification
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
        description: Two-step verification succeeded
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
      '400':
        description: Invalid or expired code
        schema:
          type: object
          properties:
            message:
              type: string
    tags:
      - auth
    """
    data = ConfirmCodeSchema().load(request.get_json())
    identity = get_jwt_identity()
    user = User.query.get(identity)
    code_from_redis = redis.redis.get(f'2_step_verification_code:{user.email}')
    if code_from_redis is not None and code_from_redis == data['code']:
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        sessions.create_session(
            user_id=user.id,
            user_agent=request.headers.get('User-Agent'),
        )
        return jsonify(
            {
              'access_token': access_token,
              'refresh_token': refresh_token,
            }
        ), HTTPStatus.OK
    return jsonify(
        {'message': 'сode is not correct or has expired'}
      ), HTTPStatus.BAD_REQUEST


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User log out
    ---
    post:
      summary: User log out
      security:
        - Bearer: []
    responses:
      '200':
        description: Logout completed
      '401':
        description: Missed authorization header
    tags:
      - auth
    produces:
      - "application/json"
    """
    jti = get_jwt()['jti']
    redis.redis.set(jti, '', ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    return jsonify({'message': 'logout completed'}), HTTPStatus.OK


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh token
    ---
    post:
      summary: Refresh token
      security:
        - Bearer: []
    responses:
      '200':
        description: Return refresh token
        schema:
          type: object
          properties:
            access_token:
              type: string
    tags:
      - auth
    """
    identity = get_jwt_identity()
    jti = get_jwt()['jti']
    redis.redis.set(jti, '', ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}), HTTPStatus.OK
