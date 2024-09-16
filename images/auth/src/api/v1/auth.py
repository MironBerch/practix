from http import HTTPStatus

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required
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


class SignUpSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, min_length=6)


class SignInSchema(SignUpSchema):
    ...


@bp.route('/signup', methods=['POST'])
def signup():
    """signup

    ---
    post:
        description: register_user
        summary: Register user
        parameters:
        - name: email
            in: path
            description: email
            schema:
            type: string
        - name: password
            in: path
            description: password
            schema:
            type: string
    responses:
        '201':
            description: Ok
        '401':
            description: Conflict
        '403':
            description: Conflict
    """
    try:
        data = SignUpSchema().load(request.get_json())
        user = User(
            email=data['email'],
            password_hash=hash_password(data['password']),
            is_active=True,
        )
        user = User.query.filter_by(email=data['email']).first()
        db.session.add(user)
        db.session.commit()
        if user is None:
            return jsonify({'message': 'User created'}), 201
        if user is not None:
            return jsonify({'message': 'User with this email exist'}), 400
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/signin', methods=['POST'])
def signin():
    """
    signin

    ---
    post:
      description: register_user
      summary: Register user
      parameters:
      - name: email
        in: path
        description: email
        schema:
          type: string
      - name: password
        in: path
        description: password
        schema:
          type: string

      requestBody:
        content:
          application/json:
            schema: UserIn
    responses:
      '201':
        description: Ok
        schema:
          $ref: "#/definitions/TokensMsg"
      '403':
        description: Incorrect password or email
        schema:
         $ref: "#/definitions/ApiResponse"
    definitions:
      ApiResponse:
        type: "object"
        properties:
          message:
            type: "string"
          status:
            type: "string"
      TokensMsg:
       type: "object"
       properties:
         message:
           type: "string"
         status:
           type: "string"
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
                {'message': 'User with this email does not exist'},
            ), HTTPStatus.BAD_REQUEST
        if not check_password(user.password, data['password']):
            return jsonify({'message': 'Password is not correct'}), HTTPStatus.FORBIDDEN
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(
            {
                'message': 'User authorized',
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        ), HTTPStatus.OK
    except ValidationError as err:
        return jsonify({'error': err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout

    ---
    post:
      description: user_logout
      summary: User logaut
      security:
        - jwt_access: []
    responses:
      '200':
        description: Logout complete
        schema:
          $ref: "#/definitions/ApiResponse"
    tags:
      - account
    produces:
      - "application/json"
    definitions:
      ApiResponse:
        type: "object"
        properties:
          message:
           type: "string"
          status:
           type: "string"
    """
    jti = get_jwt()['jti']
    redis.redis.set(jti, '', ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    return jsonify({'message': 'Session completed'}), HTTPStatus.OK
