import logging

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.logger = logging.getLogger(__name__)
    app.logger.setLevel(logging.INFO)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
