from http import HTTPStatus

from flask import Blueprint, jsonify

bp = Blueprint('health', __name__, url_prefix='/healthcheck')


@bp.route('/health', methods=['GET'])
def healthcheck():
    """
    Checking the service's health
    ---
    post:
      summary: Health check
    responses:
      '200':
        description: Server working correctly
    tags:
      - health
    produces:
      - "application/json"
    """
    return jsonify({'status': 'ok'}), HTTPStatus.OK
