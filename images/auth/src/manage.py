from flask import Flask

from core.config import settings
from core.logger import logger


def create_app() -> Flask:
    app = Flask(__name__)
    app.logger = logger
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=settings.flask.host,
        port=settings.flask.port,
        debug=settings.flask.debug,
    )
