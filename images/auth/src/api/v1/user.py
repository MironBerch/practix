from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity
from marshmallow import Schema, ValidationError, fields

from flask import Blueprint, jsonify, request

from db.postgres import db
from models.user import User
from utils.hash_password import check_password, hash_password

bp = Blueprint(
    'user',
    __name__,
    url_prefix='/user'
)


class PasswordChangeSchema(Schema):
    old_password = fields.String(required=True, min_length=6)
    new_password = fields.String(required=True, min_length=6)


class UserSchema(Schema):
    email = fields.Email(required=True)


@bp.route('/password_change', methods=['POST'])
def password_change():
    """
    Change user password

    ---
    post:
      description: password_change
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
        if not check_password(user.password_hash, data['old_password']):
            raise ValidationError('old password is not correct')
        user.password_hash = hash_password(data['new_password'])
        db.session.commit()
        return jsonify({'message': 'password changed'}), HTTPStatus.CREATED
    except ValidationError as err:
        return jsonify({'message': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/change_email', methods=['POST'])
def change_email():
    """
    Change user email

    ---
    post:
      description: change_user_email
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
        description: User
    tags:
      - user
    """
    try:
        identity = get_jwt_identity()
        data = UserSchema().load(request.get_json())
        user = User.query.get(id=identity)
        if User.query.filter_by(email=data['email']).first():
            raise ValidationError('user with this email exist')
        user.email = data['email']
        db.session.commit()
        return jsonify({'message': 'password changed'}), HTTPStatus.CREATED
    except ValidationError as err:
        return jsonify({'message': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
