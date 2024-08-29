from flask import Blueprint, jsonify

bp = Blueprint(
    'health',
    __name__,
    url_prefix='/healthcheck'
)


@bp.route('/health', methods=['GET'])
def healthcheck():
    """Проверка работоспособности сервиса."""
    return jsonify({'status': 'ok'}), 200

    #  responses={
    #      200: {
    #          'description': 'Success',
    #          'content': {
    #              'application/json': {
    #                  'example': {'status': 'ok'},
    #              },
    #          },
    #      },
    #  },
