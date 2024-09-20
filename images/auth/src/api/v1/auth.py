from http import HTTPStatus

from celery import shared_task
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import Schema, ValidationError, fields

from flask import Blueprint, current_app, jsonify, request

from db import redis
from db.postgres import db
from models.user import User
from utils.hash_password import check_password, hash_password

bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


@shared_task
def delete_user_with_not_confirmed_email(user_id):
    user = User.query.get(user_id)
    if user and not user.is_email_confirmed:
        db.session.delete(user)
        db.session.commit()


class SignUpSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, min_length=6)


class SignInSchema(SignUpSchema):
    ...


@bp.route('/signup', methods=['POST'])
def signup():
    """
    User sign up

    ---
    post:
      description: register_user
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
        user = User(
            email=data['email'],
            password_hash=hash_password(data['password']),
            is_active=True,
            is_email_confirmed=False,
        )
        if User.query.filter_by(email=data['email']).first():
            raise ValidationError('user with this email exist')
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'user created'}), HTTPStatus.CREATED
    except ValidationError as err:
        return jsonify({'message': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/email_confirm', methods=['POST'])
@jwt_required()
def email_confirm():
    delete_user_with_not_confirmed_email.apply_async(
        (get_jwt_identity(),),
        countdown=60*60,
      )


@bp.route('/signin', methods=['POST'])
def signin():
    """
    User sign in

    ---
    post:
      description: register_user
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
        description: Ok
        schema:
          $ref: "#/definitions/TokensMsg"
      '403':
        description: Incorrect password or email
        schema:
          $ref: "#/definitions/ApiResponse"
      '500':
        description: Server error
        schema:
          $ref: "#/definitions/ApiResponse"
    tags:
      - auth
    definitions:
      ApiResponse:
        type: "object"
        properties:
          message:
            type: "string"
      TokensMsg:
        type: "object"
        properties:
          access_token:
            type: "string"
          refresh_token:
            type: "string"
    """
    try:
        data = SignInSchema().load(request.get_json())
        user = User.query.filter_by(email=data['email']).first()
        if user is None:
            return jsonify(
                {'message': 'user with this email does not exist'},
            ), HTTPStatus.FORBIDDEN
        if not check_password(user.password, data['password']):
            return jsonify({'message': 'password is not correct'}), HTTPStatus.FORBIDDEN
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(
            {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        ), HTTPStatus.OK
    except ValidationError as err:
        return jsonify({'message': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User log out

    ---
    post:
      description: user_logout
      summary: User log out
      security:
        - jwt_access: []
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
      description: refresh_token
      summary: Refresh token
      security:
        - jwt_access: []
    responses:
      '200':
        description: Return refresh token
        schema:
          $ref: "#/definitions/AccessTokenMsg"
    tags:
      - auth
    definitions:
      AccessTokenMsg:
        type: "object"
        properties:
          access_token:
            type: "string"
    """
    identity = get_jwt_identity()
    jti = get_jwt()['jti']
    redis.redis.set(jti, '', ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}), HTTPStatus.OK
