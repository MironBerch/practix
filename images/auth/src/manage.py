from flask import Flask

from core.logger import logger


def create_app() -> Flask:
    app = Flask(__name__)
    app.logger = logger
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
