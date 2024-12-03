from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from flask import Blueprint, jsonify, request

from api.schemas import ConfirmCodeSchema, EmailSchema, PasswordChangeSchema, UserSessionSchema
from db import postgres, redis
from models.session import Session
from models.user import User
from utils import code, hash_password, tasks

bp = Blueprint(
    'user',
    __name__,
    url_prefix='/user'
)


@bp.route('/password_change', methods=['POST'])
@jwt_required()
def password_change():
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
        user = User.query.get(id=identity)
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
def change_email():
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
        user = User.query.get(id=identity)
        if User.query.filter_by(email=data['email']).first():
            raise ValidationError('user with this email exist')
        tasks.send_change_email_verification_code.delay(
            user.email,
            code.create_change_email_verification_code(user.email, data['email']),
        )
        return jsonify({'message': 'email changed'}), HTTPStatus.CREATED
    except ValidationError as err:
        return jsonify({'message': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/resend_change_email', methods=['POST'])
@jwt_required()
def resend_change_email():
    """
    Resend change email
    ---
    post:
      summary: Resend change email
      security:
        - jwt_access: []
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
    user = User.query.get(id=identity)
    verification_code = redis.redis.get(f'email_change:{user.email}')
    if verification_code is None:
        return jsonify({'message': 'no code for your email'}), HTTPStatus.BAD_REQUEST
    verification_code = verification_code.split(':')
    tasks.send_registration_email_verification_code.delay(
        user.email,
        code.create_change_email_verification_code(
            user.email,
            verification_code[0],
        ),
    )
    return jsonify({'message': 'code sended on email'}), HTTPStatus.OK


@bp.route('/confirm_change_email', methods=['POST'])
@jwt_required()
def confirm_change_email():
    """
    Confirm email for change with verification code
    ---
    post:
      summary: Confirm change email
      security:
        - jwt_access: []
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
    user = User.query.get(id=identity)
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
def get_user_sessions():
    """
    Get user sessions
    ---
    get:
      summary: Get user sessions
      security:
        - jwt_access: []
    responses:
      200:
        description: Return sessions
        schema:
          $ref: "#/definitions/UserSession"
      403:
        description: Forbidden error
        schema:
          $ref: "#/definitions/ApiResponse"
    definitions:
      ApiResponse:
        type: "object"
        properties:
          message:
            type: "string"
      UserSession:
        type: "object"
        properties:
          data:
            type: "object"
            properties:
              user_id:
                type: "string"
                format: "uuid"
              user_agent:
                type: "string"
              user_device_type:
                type: "string"
              date:
                type: "string"
                format: "date"
    tags:
      - user
    """
    identity = get_jwt_identity()
    user = User.query.get(id=identity)
    paginated_user_sessions = Session.query.filter_by(user_id=user.id).paginate(
        page=request.args.get('page', default=1, type=int),
        per_page=request.args.get('count', default=10, type=int),
    )
    return (
        jsonify(
            {
                'sessions': UserSessionSchema().dump(
                    paginated_user_sessions.items,
                    many=True,
                ),
            }
        ),
        HTTPStatus.OK,
    )
